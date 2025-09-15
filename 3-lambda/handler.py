import os
import json
import base64
import uuid
import boto3
import io
from datetime import datetime
from PIL import Image

s3 = boto3.client("s3")

INPUT_BUCKET = os.environ.get("INPUT_BUCKET", "")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "")

def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",           # 브라우저 테스트용
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }

def lambda_handler(event, context):
    try:
        if (not INPUT_BUCKET) or (not OUTPUT_BUCKET):
            return _resp(400, {"error": "S3 bucket env not set: INPUT_BUCKET/OUTPUT_BUCKET"})

        if event.get("httpMethod") == "OPTIONS":
            # CORS preflight
            return _resp(200, {"ok": True})

        if "body" not in event:
            return _resp(400, {"error": "no body"})

        # --- 이미지 바이트 추출 ---
        try:
            if event.get("isBase64Encoded"):
                img_bytes = base64.b64decode(event["body"])
            else:
                # 텍스트 본문을 base64 문자열로 간주(프론트가 base64로 넘긴 경우)
                img_bytes = base64.b64decode(event["body"].encode("utf-8"))
        except Exception as e:
            return _resp(400, {"error": f"invalid image/base64: {e}"})

        # --- 파일 메타 ---
        ext = "jpg"
        ctype = "image/jpeg"
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        uid = uuid.uuid4().hex

        # --- 원본 저장 ---
        in_key = f"uploads/{ts}-{uid}.{ext}"
        s3.put_object(Bucket=INPUT_BUCKET, Key=in_key, Body=img_bytes, ContentType=ctype)

        # --- 흑백 변환 ---
        img = Image.open(io.BytesIO(img_bytes)).convert("L")
        out_buf = io.BytesIO()
        img.save(out_buf, format="JPEG")
        out_buf.seek(0)

        # --- 결과 저장 ---
        out_key = f"results/{ts}-{uid}-gray.{ext}"
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=out_key, Body=out_buf.getvalue(), ContentType=ctype)

        # --- presigned URL ---
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": OUTPUT_BUCKET, "Key": out_key},
            ExpiresIn=1800  # 30분
        )

        return _resp(200, {
            "input_key": in_key,
            "output_key": out_key,
            "download_url": url
        })

    except Exception as e:
        # 콘솔 로그에는 스택트레이스가 남음
        return _resp(500, {"error": f"internal error: {type(e).__name__}: {e}"})
