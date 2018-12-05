import cv2
import sys
from random import randint
import math

class Tracker():
  tracker_type = ""
  bboxes = []
  colors = []
  frame_width = 0.0
  camera_distance = 0.0
  focal_distance = 0.0
  field_view = 0.0
  frame_width_m = 0.0
  m_pixel = 0.0
  fact_km_h = 0.0
  frame_time = 0.0
  video_fps = 0.0
  frame_time = 0.0

  def init_parameters(self):
    # calculate the camera distance
    # Distance camera - object. Unit m
    self.camera_distance = 13.435
    #Focal length, unit: m
    self.focal_distance = 0.0039
    #The field of view of the camera. Unit: degrees Celsius
    self.field_view = 69
    #The horizontal distance covered by the image at a distance. Unit: m
    self.frame_width_m = round(2*(math.tan(math.radians(self.field_view*0.5))*self.camera_distance),3)
    self.m_pixel = round(self.frame_width_m/self.frame_width,5)
    self.fact_km_h = 3600.0
    self.frame_time = 1000/self.video_fps

  def create_tracker(self):
    self.tracker_type = "KCF"
    # Create a tracker
    tracker = cv2.TrackerKCF_create()
    return tracker

  def open_video(self, path):
    #Open video
    video = cv2.VideoCapture(path)
    #Exit if video not opened
    if not video.isOpened():
      print("No se puede abrir el video")
      sys.exit()
    self.frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.video_fps = video.get(cv2.CAP_PROP_FPS)
    return video

  def simple_tracker(self, path):
    video = self.open_video(path)
    self.init_parameters()
    # Read first frame.
    ok, frame = video.read()
    old_frame = frame
    if not ok:
      print('No se puede leer el archivo de video')
      sys.exit()
    #Create points of instant velocity
    feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 7,blockSize = 7 )
    lk_params = dict(winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    #Create tracker
    tracker = self.create_tracker()
    #Def bounding box by user
    bbox = cv2.selectROI(frame, False)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    velocity_list = []
    while True:
      # Read a new frame
      ok, frame = video.read()
      if not ok:
        break
      # Start timer
      #timer = cv2.getTickCount()
      #
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
      good_new = p1[st==1]
      good_old = p0[st==1]
      for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        if a > bbox[0] and a < (bbox[0]+bbox[2]) and b > bbox[1] and b < (bbox[1]+bbox[3]):
          vel_ins = self.get_velocity_ins(a,b,c,d)
          velocity_list.append(vel_ins)
      vel_ins_average = round(self.average_list(velocity_list),2)
      bbox_old = bbox
      # Update tracker
      ok, bbox = tracker.update(frame)
      other_vel_ins_average = round(self.get_velocity_ins(bbox_old[0],bbox_old[1],bbox[0],bbox[1]),2)
      # Calculate Frames per second (FPS)
      #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
      # Draw bounding box
      if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        #cv2.circle(frame,p1,5,(0,255,0) ,-1)
        #cv2.circle(frame,p2,5,(0,255,0) ,-1)
      else :
        # Tracking failure
        cv2.putText(frame, "Error...", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
      # Display tracker type on frame
      cv2.putText(frame, "Velocidad Tracker" + str(other_vel_ins_average), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
      # Display FPS on frame
      cv2.putText(frame, "Velocidad TK: " + str(vel_ins_average), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
      # Display result
      cv2.imshow("Tracking", frame)
      # Exit if ESC pressed
      k = cv2.waitKey(1) & 0xff
      if k == 27 : break
      velocity_list = []

  def get_velocity_ins(self,x1,y1,x2,y2):
    #Euclidean distance
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #Instant velocity of the object
    instant_velocity = distance/self.frame_time * self.m_pixel * self.fact_km_h
    return instant_velocity

  def average_list(self, el_list):
    sum=0.0
    for i in range(0,len(el_list)):
        sum=sum+el_list[i]
    if len(el_list) > 0:
      return sum/len(el_list)
    else:
      return 0

if __name__ == '__main__' :
  mytra = Tracker()
  mytra.simple_tracker("150291160.avi")
