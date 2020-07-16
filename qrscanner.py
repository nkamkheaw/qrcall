import PIL
import cv2
import requests
import zbarlight

video_capture = cv2.VideoCapture(1)
call_set = set()

def get_webcam_image():
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    cv2.imshow("Webcam", frame)

    # Convert the CV frame to PIL image
    return PIL.Image.fromarray(frame)


def decode_image(image):
    # Decode the QR code in PIL image
    return zbarlight.scan_codes('qrcode', image)


def make_http_call(url):
    if url in call_set:
        print(f"{url} is called: ignore it.")
        return

    r = requests.get(url)

    if r.status_code == 200:
        print(f"Successfully requests to {url}")
        call_set.add(url)


if __name__ == '__main__':

    while True:
        image = get_webcam_image()
        decode_value = decode_image(image)

        if decode_value:
            for value in decode_value:
                make_http_call(value)

        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

