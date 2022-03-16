import cv2 
import numpy as np 
import tensorflow as tf
import os
import easyocr
import schedule
import time
import json 

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util


# gpus = tf.config.list_physical_devices("GPU")
# if gpus:
#     try:
#         tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=5120)])
#     except RuntimeError as e:
#         print(f"Błąd: {e}")

prefix = os.getcwd()
db = f"{prefix}/DataBase.json"

configs = config_util.get_configs_from_pipeline_file(os.path.join("AIData", "pipeline.config"))
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join("AIData", 'ckpt-11')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def detect_plate(car_number):
    IMAGE_PATH = os.path.join("AIData", 'test', f'Cars{car_number}.png')

    img = cv2.imread(IMAGE_PATH)
    image_np = np.array(img)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections


    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    category_index = label_map_util.create_category_index_from_labelmap(os.path.join("AIData", "label_map.pbtxt"))

    viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=.8,
                agnostic_mode=False)

    return image_np_with_detections, detections, category_index

def text_filtering(region, ocr_results, region_treshold):
    rectangle_size = region.shape[0]*region.shape[1]

    plate = []
    for result in ocr_results:
        lenght = np.sum(np.subtract(result[0][1], result[0][0]))
        height = np.sum(np.subtract(result[0][2], result[0][1]))

        if lenght*height / rectangle_size > region_treshold:
            plate.append(result[1])
    return plate 


   

def get_registration_numbers(image, detections, detection_threshold, region_treshold, text_threshold):

    scores = list(filter(lambda x: x > detection_threshold, detections["detection_scores"]))
    boxes = detections["detection_boxes"][:len(scores)]
    classes = detections["detection_classes"][:len(scores)]

    width= image.shape[1]
    height = image.shape[0]

    region = None
    text = None
    for _, box in enumerate(boxes):
        roi = box*[height, width, height, width] #region of interest
        region = image[int(roi[0]):int(roi[2]), int(roi[1]): int(roi[3])]
        reader = easyocr.Reader(['en'])
        ocr_results = reader.readtext(region, text_threshold=text_threshold)

    if region is not None:
        text = text_filtering(region, ocr_results, region_treshold)
    return text, region

def AImain():
    
    detection_threshold = 0.4
    region_treshold = 0.6
    text_threshold = 0.7

    with open(db, "r", encoding="utf-8") as file:
        data = json.load(file)
        images = data["db"]["cameras"]

    for car_nr in images:
        image_np_with_detections, detections, _ = detect_plate(car_number=car_nr)
        image = image_np_with_detections
        text, _ = get_registration_numbers(image, detections, detection_threshold, region_treshold, text_threshold)
        if text:
            text = text[0].upper()
        
            with open(db, "r", encoding="utf-8") as file:
                data = json.load(file)
                P_cars_registrations = data["db"]["cars"]["registrations"]
                camera = data["db"]["cars"]["camera"]

                if not text in P_cars_registrations:
                    cameras = data["db"]["cameras"]
                    idx = cameras.index(car_nr)
                    places = data["db"]["places"]
                    place = places[idx]  

                    P_cars_registrations.append(text)
                    C_cars_registrations = P_cars_registrations
                
                    P_cars_locations = data["db"]["cars"]["locations"]
                    P_cars_locations.append(place)
                    C_cars_locations = P_cars_locations

                    camera.append(car_nr)

                    with open(db, "w", encoding="utf-8") as file_w:
                        data["db"]["cars"]["registrations"] = C_cars_registrations
                        data["db"]["cars"]["locations"] = C_cars_locations
                        data["db"]["cars"]["camera"] = camera
                        json.dump(data, file_w, ensure_ascii=False, indent=4)
                    file_w.close()

            file.close()

        
    
def AImanager():
    schedule.every(1).minutes.do(AImain)
    AImain()
    while True:
        schedule.run_pending()
        time.sleep(10)
    

"""
images = ["400", "401", "402", "403", "412"]
plates = []

detection_threshold = 0.4
region_treshold = 0.6
text_threshold = 0.7

for image in images:
    image_np_with_detections, detections, category_index = detect_plate(image)
    image = image_np_with_detections


    text, region = get_registration_numbers(image, detections, detection_threshold, region_treshold, text_threshold)
    if text:
        text = text[0]
    
    plates.append(text)


print(images, plates)
"""

# cap = cv2.VideoCapture("test1.mp4")
# cap.set(3, 1920)
# cap.set(4, 1080)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# while cap.isOpened(): 
#     ret, frame = cap.read()
#     image_np = np.array(frame)
    
#     input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
#     detections = detect_fn(input_tensor)
    
#     num_detections = int(detections.pop('num_detections'))
#     detections = {key: value[0, :num_detections].numpy()
#                   for key, value in detections.items()}
#     detections['num_detections'] = num_detections

#     # detection_classes should be ints.
#     detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

#     label_id_offset = 1
#     image_np_with_detections = image_np.copy()

#     viz_utils.visualize_boxes_and_labels_on_image_array(
#                 image_np_with_detections,
#                 detections['detection_boxes'],
#                 detections['detection_classes']+label_id_offset,
#                 detections['detection_scores'],
#                 category_index,
#                 use_normalized_coordinates=True,
#                 max_boxes_to_draw=5,
#                 min_score_thresh=.3,
#                 agnostic_mode=False)

#     try:
#         text, region = get_registration_numbers(image_np_with_detections, detections, detection_threshold, region_treshold, text_threshold)
#         print(f"Here: {text[0]}")
#     except:
#         pass 

#     cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
    
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         cap.release()
#         cv2.destroyAllWindows()
#         break