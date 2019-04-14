import cv2
import glob
import random

from shutil import copyfile

class FacialEmotionRecognition:

    def __init__(self):
        self.emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
        self.source_emotion = "emotion"
        self.source_image = "images"
        self.neutral = "neutral"
        self.sorted_emotion = "sorted_emotion_set"
        self.face_detection_filter_1 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.face_detection_filter_2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        self.face_detection_filter_3 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
        self.face_detection_filter_4 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.filtered_dataset = "filtered_face_dataset"
        self.image_format = "jpg"


    def pre_process_data(self):
        volunteers = sorted(glob.glob("%s/*" %self.source_emotion))
        for volunteer in volunteers:
            volunteer_id = volunteer[-4:]
            for session in sorted(glob.glob("%s/*" %volunteer)):
                session_id = session[13:17]
                for file_name in sorted(glob.glob("%s/*"  %session)):
                    file = open(file_name, 'r')
                    emotion_number = int(float(file.readline()))
                    source_emotion_file = sorted(glob.glob("%s/%s/%s/*" %(self.source_image, volunteer_id, session_id)))[-1]
                    source_neutral_file = sorted(glob.glob("%s/%s/%s/*" %(self.source_image, volunteer_id, session_id)))[0]
                    dest_neutral_file = "%s/%s/%s" %(self.sorted_emotion, self.neutral, source_neutral_file[16:])
                    dest_emotion_file = "%s/%s/%s" %(self.sorted_emotion, self.emotions[emotion_number], source_emotion_file[16:])
                    copyfile(source_neutral_file, dest_neutral_file)
                    copyfile(source_emotion_file, dest_emotion_file)


    def filter_faces_from_dataset(self):

        for emotion in self.emotions:

            files = sorted(glob.glob("%s/%s/*" %(self.sorted_emotion, emotion)))

            for num, file in enumerate(files, 0):
                image = cv2.imread(file)
                gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                face_1 = self.face_detection_filter_1.detectMultiScale(gray_scale, scaleFactor = 1.1, minNeighbors = 10,
                                                                       minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
                face_2 = self.face_detection_filter_2.detectMultiScale(gray_scale, scaleFactor=1.1, minNeighbors=10,
                                                                       minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
                face_3 = self.face_detection_filter_3.detectMultiScale(gray_scale, scaleFactor=1.1, minNeighbors=10,
                                                                       minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
                face_4 = self.face_detection_filter_4.detectMultiScale(gray_scale, scaleFactor=1.1, minNeighbors=10,
                                                                       minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

                if len(face_1) == 1:
                    face_features = face_1
                elif len(face_2) == 1:
                    face_features = face_2
                elif len(face_3) == 1:
                    face_features = face_3
                elif len(face_4) == 1:
                    face_features = face_4
                else:
                    face_features = ""

                for (x, y, w, h) in face_features:
                    gray_scale = gray_scale[y:y+h, x:x+w]
                    try:
                        output_image = cv2.resize(gray_scale, (350, 350))
                        cv2.imwrite("%s/%s/%s.%s" %(self.filtered_dataset, emotion, num, self.image_format), output_image)
                    except:
                        pass


    def train_predict_dataset_split(self, emotion):
        files = sorted(glob.glob("%s/%s/*" %(self.sorted_emotion, emotion)))
        random.shuffle(files)
        training_set = files[0:int(len(files)*0.80)]
        prediction_set = files[-int(len(files)*0.20)]
        return training_set, prediction_set


    def convert_set_images_to_grayscale_and_append_data_label(self, test_set, emotion):
        data_set = []
        label_set = []
        for item in test_set:
            img = cv2.imread(item)
            img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            data_set.append(img_grayscale)
            label_set.append(emotion)
        return data_set, label_set


    def generate_data_and_labels(self):
        training_data_set = []
        training_label_set = []
        prediction_data_set = []
        prediction_label_set = []

        for emotion in self.emotions:

            train_set, predict_set = self.train_predict_dataset_split(emotion)

            training_data, training_label = self.convert_set_images_to_grayscale_and_append_data_label(train_set, emotion)
            training_data_set.append(training_data)
            training_label_set.append(training_label)

            prediction_data, prediction_label = self.convert_set_images_to_grayscale_and_append_data_label(predict_set, emotion)
            prediction_data_set.append(prediction_data)
            prediction_label_set.append(prediction_label)

        return training_data_set,training_label_set, prediction_data_set, prediction_label_set


if __name__ == '__main__':
    fer = FacialEmotionRecognition()
    # fer.pre_process_data()
    # fer.filter_faces_from_dataset()
    fer.generate_data_and_labels()