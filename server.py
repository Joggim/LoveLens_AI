from flask import Flask, request, jsonify
from flask_cors import CORS
from face_verification import decode_image, verify_face

app = Flask(__name__)
CORS(app)

PROFILE_IMAGE_PATH = "your_face.jpg" # 사용자가 업로드한 이미지 경로

@app.route("/verify", methods=["POST"])
def verify():
    try:
        # 프론트엔드에서 전송된 이미지 가져오기
        data = request.get_json()
        image_data = data.get("image", None)

        if not image_data:
            return jsonify({"success": False, "message": "이미지가 전송되지 않았습니다."}), 400

        input_image = decode_image(image_data)

        input_image_path = "input_image.jpg"
        input_image.save(input_image_path)
        print(f"입력 이미지 저장 완료: {input_image_path}")

        result = verify_face(input_image_path, PROFILE_IMAGE_PATH)

        # 결과 반환
        if result["success"]:
            if result["verified"]:
                return jsonify({"success": True, "message": "본인 확인 성공!", "distance": result["distance"]})
            else:
                return jsonify({"success": False, "message": "본인 확인 실패!", "distance": result["distance"]})
        else:
            return jsonify({"success": False, "message": result["message"]})

    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"success": False, "message": "서버 처리 중 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
