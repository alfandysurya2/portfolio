from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve, auc

def split_and_prepare_mnist_dataset(df, test_size=0.2, random_state=42):
    X = df.drop('label', axis=1).to_numpy()
    y = df['label'].to_numpy()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    X_train = X_train.astype(np.float64)
    X_test = X_test.astype(np.float64)
    y_train = y_train.astype(np.uint8)
    y_test = y_test.astype(np.uint8)
    
    return X, y, X_train, X_test, y_train, y_test

def plot_images(instances, images_per_row=10, **options):
    size = 28
    images_per_row = min(len(instances), images_per_row)
    n_rows = (len(instances) - 1) // images_per_row + 1
    n_empty = n_rows * images_per_row - len(instances)
    padded_instances = np.concatenate([instances, np.zeros((n_empty, size * size))], axis=0)
    image_grid = padded_instances.reshape((n_rows, images_per_row, size, size))
    big_image = image_grid.transpose(0, 2, 1, 3).reshape(n_rows * size, images_per_row * size)
    plt.imshow(big_image, cmap = mpl.cm.binary, **options)
    plt.axis("off")
    
def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fontsize=13)
    plt.xlabel("Threshold", fontsize=13)
    plt.ylabel('Value', fontsize=13)
    plt.grid(True)                           
    plt.axis([0, 1, 0, 1])

def plot_precision_vs_recall(precisions, recalls, label=None):
    plt.plot(recalls, precisions, "b-", label=label, linewidth=2)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fontsize=13)
    plt.xlabel("Recall", fontsize=13)
    plt.ylabel("Precision", fontsize=13)
    plt.axis([0, 1, 0, 1])
    plt.grid(True)
    
def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('FPR', fontsize=13)
    plt.ylabel('TPR', fontsize=13)
    plt.grid(True)

def plot_multiclass_roc_curve(y, y_train, y_score, label):
    random_state = np.random.RandomState(0)
    n_classes = len(np.unique(y))
    target_names = np.array(label['fashion_name'])
    label_binarizer = LabelBinarizer().fit(y_train)
    y_onehot_test = label_binarizer.transform(y_train)
    y_onehot_test.shape
    
    fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
    # store the fpr, tpr, and roc_auc for all averaging strategies
    fpr, tpr, roc_auc = dict(), dict(), dict()
    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_onehot_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_onehot_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    fpr_grid = np.linspace(0.0, 1.0, 1000)

    # Interpolate all ROC curves at these points
    mean_tpr = np.zeros_like(fpr_grid)

    for i in range(n_classes):
        mean_tpr += np.interp(fpr_grid, fpr[i], tpr[i])  # linear interpolation

    # Average it and compute AUC
    mean_tpr /= n_classes

    fpr["macro"] = fpr_grid
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    plt.plot(
        fpr["micro"],
        tpr["micro"],
        label=f"micro-average ROC curve (AUC = {roc_auc['micro']:.2f})",
        color="deeppink",
        linestyle=":",
        linewidth=4,
    )

    plt.plot(
        fpr["macro"],
        tpr["macro"],
        label=f"macro-average ROC curve (AUC = {roc_auc['macro']:.2f})",
        color="navy",
        linestyle=":",
        linewidth=4,
    )

    def get_cmap(n, name='tab10'):
        return plt.cm.get_cmap(name, n)

    cmap = get_cmap(n_classes)
    for class_id in range(n_classes):
        i = int(class_id)
        RocCurveDisplay.from_predictions(
            y_onehot_test[:, class_id],
            y_score[:, class_id],
            name=f"ROC curve for class {i} : {target_names[class_id]}",
            color=cmap(class_id),
            ax=ax,
        )

    plt.plot([0, 1], [0, 1], "k--", label="ROC curve for chance level (AUC = 0.5)")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fontsize=10)
    
def precision_recall_vs_threshold_df(threshold, precision, recall):
    p = pd.Series(precision, name='precision')
    r = pd.Series(recall, name='recall')
    t = pd.Series(threshold, name='prediction_probability')
    df = pd.concat([t, p, r], axis=1)
    return df

