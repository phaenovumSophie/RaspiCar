""" raspicar_camera.py

SLW 01-23-2023
"""

import time
import cv2

class CameraMeans:
    
    def __init__(self, width=800, height=600, rows = 4, cols = 6):
        # Calculate parameters
        self.width, self.height = width, height
        self.rows, self.cols = rows, cols
        self.x_boundaries = [i * self.width // cols for i in range(cols + 1)]
        self.y_boundaries = [i * self.height // rows for i in range(rows + 1)]
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.x_offset, self.y_offset = 10, 30
        # Start video capture
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.error = False
        
    def get_frame(self):
        _, frame = self.vid.read()
        return frame
    
    def get_means(self, show_image = False):
        if self.error:
            return([0 for _ in range(self.rows * self.cols)])

        res, frame = self.vid.read()

        if not res:
            print("Video stream read errror")
            self.vid.release()
            self.error = True
            return([0 for _ in range(self.rows * self.cols)])

        # Calculate mean values for each cell
        reduced_frame = cv2.resize(frame, (self.cols, self.rows), interpolation=cv2.INTER_LINEAR)
        means = reduced_frame.mean(axis=2).flatten()
        means = (means - means.mean()).round().astype(int)

        if show_image:
            # draw grid to frame
            for row in range(1, self.rows):
                cv2.line(frame, (0, self.y_boundaries[row]), (self.width, self.y_boundaries[row]), (255, 255, 255))
            for col in range(1, self.cols):
                cv2.line(frame, (self.x_boundaries[col], 0), (self.x_boundaries[col], self.height), (255, 255, 255))
            # draw mean values to frame
            cnt = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    cv2.putText(frame, str(round(means[cnt])),
                                (self.x_boundaries[col] + self.x_offset, self.y_boundaries[row] + self.y_offset),
                                self.font, 1, (255, 255, 255), 2)
                    cnt += 1
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
        
        return means
    
    def show_frame(self):
        res, frame = self.vid.read()

        if not res:
            print("Video stream read errror")
            self.vid.release()
            self.error = True
            return
            
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        return
          
    
    def close(self):
        self.vid.release()
        cv2.destroyAllWindows()

#=================================================================================

duration = []

if __name__ == "__main__":
    cam = CameraMeans()
    
    for i in range(200):
        start_time = time.time()
        #cam.show_frame()
        values = cam.get_means(show_image=True)
        duration.append(time.time() - start_time)
        # print(values)
        time.sleep(0.1)
                    
    cam.close()
    
    print(round(1000 * sum(duration) / 200, 2), "ms")
        
