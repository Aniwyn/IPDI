import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt

from rasterio.mask import mask
from shapely.geometry import mapping
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


archivo_tif = "D:\\Aniwyn\\Documents\\PyCharm\\IPDI\\src\\tp_final\\05-21_raster3.tif"
archivo_gpkg = "D:\\Aniwyn\\Documents\\PyCharm\\IPDI\\src\\tp_final\\05-21_datos etiquetados2.gpkg"

with rasterio.open(archivo_tif) as src:
    X = np.array([], dtype=np.int8).reshape(0, src.count)
    y = np.array([], dtype=np.string_)

    band_count = src.count
    print(band_count)

    shape_file = gpd.read_file(archivo_gpkg)
    shape_file = shape_file.to_crs(src.crs)
    geoms = shape_file.geometry.values

    for index, geom in enumerate(geoms):
        single_polygon = list(geom.geoms)[0]
        feature = [mapping(single_polygon)]

        try:
            out_image, out_transform = mask(src, feature, crop=True)
        except ValueError as e:
            print(f"Error processing geometry {index}: {e}")
            continue

        out_image_reshape = out_image.reshape(-1, band_count)

        y = np.append(y, [shape_file["class"][index]] * out_image_reshape.shape[0])
        X = np.vstack((X, out_image_reshape))

    labels = np.unique(shape_file["class"])
    labels2 = np.unique(shape_file["className"])
    print(labels)
    print(labels2)

    print(X.shape, " ", y.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print(X_train.shape, " ", X_test.shape)
    print(y_train.shape, " ", y_test.shape)

    clf = RandomForestClassifier(n_estimators=3000, min_samples_leaf=50, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print("Classification Report:")
    print(classification_rep)
