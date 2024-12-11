from deepface import DeepFace
from PIL import Image
import base64
import io

def decode_image(base64_image):
    image_data = base64.b64decode(base64_image.split(",")[1])
    return Image.open(io.BytesIO(image_data))


def verify_face(input_image_path, profile_image_path):
    try:
        # DeepFace로 얼굴 비교
        result = DeepFace.verify(
            img1_path=profile_image_path,
            img2_path=input_image_path,
            enforce_detection=False,
            model_name="Facenet",
            distance_metric="cosine"
        )

        # 결과 리턴
        return {
            "success": True,
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
        }
    except Exception as e:
        print(f"본인 확인 중 오류 발생: {e}")
        return {"success": False, "message": "본인 확인 중 오류가 발생했습니다."}

