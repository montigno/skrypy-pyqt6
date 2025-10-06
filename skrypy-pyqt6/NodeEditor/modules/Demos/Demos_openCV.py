class openCV_camera():

    def __init__(self, rect=(100, 100, 300, 300), filter="enumerate(('Canny', 'Schtroumpf'))"):
        import cv2

        self.rect = rect
        self.delta_x, self.delta_y = rect[2] - rect[0], rect[3] - rect[1]
        cam_capture = cv2.VideoCapture(0)
        cv2.destroyAllWindows()
        self.upper_left = (rect[0], rect[1])
        self.bottom_right = (rect[2], rect[3])
        self.click_hold = False

        def __sketch_transform(image):
            image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (7, 7), 0)
            image_canny = cv2.Canny(image_grayscale_blurred, 10, 80)
            _, mask = cv2.threshold(image_canny, 30, 255, cv2.THRESH_BINARY_INV)
            return mask

        def __moveWindow(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if (x >= self.upper_left[0] and x <= self.bottom_right[0] and
                        y >= self.upper_left[1] and y <= self.bottom_right[1]):
                    self.click_hold = True
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.click_hold:
                    if (x >= 0 and x <= cv2.getWindowImageRect('camera')[2] and y >= 0 and y <= cv2.getWindowImageRect('camera')[3]):
                        self.upper_left = (x, y)
                        self.bottom_right = (x + self.delta_x, y + self.delta_y)
                    else:
                        self.click_hold = False
            elif event == cv2.EVENT_LBUTTONUP:
                self.click_hold = False

        cv2.namedWindow('camera')
        cv2.setMouseCallback('camera', __moveWindow)

        while True:
            _, image_frame = cam_capture.read()
            image_frame = cv2.flip(image_frame, 1)
            r = cv2.rectangle(image_frame, self.upper_left, self.bottom_right, (100, 150, 200), 0)
            cv2.putText(image_frame, 'press Esc to exit', (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            rect_img = image_frame[self.upper_left[1]: self.bottom_right[1], self.upper_left[0]: self.bottom_right[0]]
            image_rect = rect_img
            if filter == 'Canny':
                image_rect = __sketch_transform(image_rect)
                image_rect_rgb = cv2.cvtColor(image_rect, cv2.COLOR_GRAY2RGB)
            elif filter == 'Schtroumpf':
                image_rect_rgb = cv2.cvtColor(image_rect, cv2.COLOR_RGB2BGR)
            image_frame[self.upper_left[1]: self.bottom_right[1], self.upper_left[0]: self.bottom_right[0]] = image_rect_rgb
            cv2.imshow("camera", image_frame)

            if cv2.waitKey(1) == 27:
                break

        cam_capture.release()
        cv2.destroyAllWindows()

##############################################################################


class openCV_screen():

    def __init__(self, rect=(100, 100, 300, 300), filter="enumerate(('NoFilter', 'Canny'))"):

        import numpy as np
        import cv2
        from mss import mss
        from PIL import Image

        mon = {'left': rect[0], 'top': rect[1], 'width': rect[2], 'height': rect[3]}

        def __sketch_transform(image):
            image_grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
            image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (7, 7), 0)
            image_canny = cv2.Canny(image_grayscale_blurred, 10, 80)
            _, mask = cv2.threshold(image_canny, 30, 512, cv2.THRESH_BINARY_INV)
            return mask

        def __real_color(image):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image_rgb

        with mss() as sct:
            while True:
                screenShot = sct.grab(mon)
                img = Image.frombytes(
                    'RGB',
                    (screenShot.width, screenShot.height),
                    screenShot.rgb,
                    )
                if filter == 'NoFilter':
                    sketcher_rect = __real_color(np.array(img))
                else:
                    sketcher_rect = __sketch_transform(np.array(img))
                cv2.imshow('test', sketcher_rect)
                if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
                    break
            cv2.destroyAllWindows()
