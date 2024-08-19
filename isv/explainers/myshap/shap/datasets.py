import os
from urllib.request import urlretrieve

import numpy as np
import pandas as pd
import sklearn.datasets

import shap

github_data_url = "https://github.com/shap/shap/raw/master/data/"


def imagenet50(resolution=224, n_points=None):
    """Return a set of 50 images representative of ImageNet images.

    Parameters
    ----------
    resolution : int
        The resolution of the images. At present the only supported value is 224.
    n_points : int, optional
        Number of data points to sample. If None, the entire dataset is used.

    Returns
    -------
    Tuple of numpy array representing images and numpy array representing the labels.

    Notes
    -----
    This dataset was collected by randomly finding a working ImageNet link and then pasting the
    original ImageNet image into Google image search restricted to images licensed for reuse. A
    similar image (now with rights to reuse) was downloaded as a rough replacement for the original
    ImageNet image. The point is to have a random sample of ImageNet for use as a background
    distribution for explaining models trained on ImageNet data.

    Note that because the images are only rough replacements, the labels might no longer be correct.

    Examples
    --------
    To get the processed images and labels::

        images, labels = shap.datasets.imagenet50()
    """
    prefix = github_data_url + "imagenet50_"
    X = np.load(cache(f"{prefix}{resolution}x{resolution}.npy")).astype(np.float32)
    y = np.loadtxt(cache(f"{prefix}labels.csv"))

    if n_points is not None:
        X = shap.utils.sample(X, n_points, random_state=0)
        y = shap.utils.sample(y, n_points, random_state=0)

    return X, y

def california(n_points=None):
    """Return the California housing data in a structured format.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to sample. If provided, randomly samples the specified number of points.

    Returns
    -------
    Tuple of pandas DataFrame containing the data and a numpy array representing the target.
        The data include the following features:

        * ``MedInc`` : Median income in block
        * ``HouseAge`` : Median house age in block
        * ``AveRooms`` : Average rooms in dwelling
        * ``AveBedrms`` : Average bedrooms in dwelling
        * ``Population`` : Block population
        * ``AveOccup`` : Average house occupancy
        * ``Latitude`` : House block latitude
        * ``Longitude`` : House block longitude

        The target column represents the median house value for California districts.

    References
    ----------
    California housing dataset: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html

    Examples
    --------
    To get the processed data and target labels::

        data, target = shap.datasets.california()
    """
    d = sklearn.datasets.fetch_california_housing()
    df = pd.DataFrame(data=d.data, columns=d.feature_names)
    target = d.target

    if n_points is not None:
        df = shap.utils.sample(df, n_points, random_state=0)
        target = shap.utils.sample(target, n_points, random_state=0)

    return df, target



def linnerud(n_points=None):
    """Return the Linnerud dataset in a convenient package for multi-target regression.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to include. Default is None, including all data points.

    Returns
    -------
    Tuple of pandas DataFrames containing the feature matrix and the target variables.

    Notes
    -----
    - The Linnerud dataset contains physiological and exercise data for 20 individuals.0
    - The feature matrix includes three exercise variables: Chins, Situps, Jumps.
    - The target variables include three physiological measurements: Weight, Waist, Pulse.

    More details: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_linnerud.html

    Examples
    --------
    To get the feature matrix and target variables::

        features, targets = shap.datasets.linnerud()

    To get a subset of the data::

        subset_features, subset_targets = shap.datasets.linnerud(n_points=100)

    """
    d = sklearn.datasets.load_linnerud()
    X = pd.DataFrame(d.data, columns=d.feature_names)
    y = pd.DataFrame(d.target, columns=d.target_names)

    if n_points is not None:
        X = shap.utils.sample(X, n_points, random_state=0)
        y = shap.utils.sample(y, n_points, random_state=0)

    return X, y


def imdb(n_points=None):
    """Return the classic IMDB sentiment analysis training data in a nice package.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to sample. If None, the entire dataset is used.

    Returns
    -------
    Tuple of list containing text data and numpy array representing the labels.

    Notes
    -----
    Full data is at: http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

    Paper to cite when using the data is: http://www.aclweb.org/anthology/P11-1015

    Examples
    --------
    To get the processed text data and labels::

        text_data, labels = shap.datasets.imdb()

    """
    with open(cache(github_data_url + "imdb_train.txt"), encoding="utf-8") as f:
        data = f.readlines()
    y = np.ones(25000, dtype=bool)
    y[:12500] = 0

    if n_points is not None:
        data = shap.utils.sample(data, n_points, random_state=0)
        y = shap.utils.sample(y, n_points, random_state=0)

    return data, y


def communitiesandcrime(n_points=None):
    """Predict the total number of non-violent crimes per 100K population.

    This dataset is from the classic UCI Machine Learning repository:
    https://archive.ics.uci.edu/ml/datasets/Communities+and+Crime+Unnormalized

    Parameters
    ----------
    n_points : int, optional
        Number of data points to sample. If provided, randomly samples the specified number of points.

    Returns
    -------
    Tuple of pandas DataFrame containing the predictive features and a numpy array representing the target.

    Examples
    --------
    To get the processed data and target labels::

        data, target = shap.datasets.communitiesandcrime()

    """
    raw_data = pd.read_csv(
        cache(github_data_url + "CommViolPredUnnormalizedData.txt"),
        na_values="?"
    )

    # find the indices where the total violent crimes are known
    valid_inds = np.where(np.invert(np.isnan(raw_data.iloc[:,-2])))[0]

    if n_points is not None:
        valid_inds = shap.utils.sample(valid_inds, n_points, random_state=0)

    y = np.array(raw_data.iloc[valid_inds,-2], dtype=float)

    # extract the predictive features and remove columns with missing values
    X = raw_data.iloc[valid_inds,5:-18]
    valid_cols = np.where(np.isnan(X.values).sum(0) == 0)[0]
    X = X.iloc[:,valid_cols]

    return X, y


def diabetes(n_points=None):
    """Return the diabetes data in a nice package.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to sample. If None, the entire dataset is used.

    Returns
    -------
    Tuple of pandas DataFrame containing the features and a numpy array representing the target.

        Feature Columns:

        - ``age`` (float): Age in years
        - ``sex`` (float): Sex
        - ``bmi`` (float): Body mass index
        - ``bp`` (float): Average blood pressure
        - ``s1`` (float): Total serum cholesterol
        - ``s2`` (float): Low-density lipoproteins (LDL cholesterol)
        - ``s3`` (float): High-density lipoproteins (HDL cholesterol)
        - ``s4`` (float): Total cholesterol / HDL cholesterol ratio
        - ``s5`` (float): Log of serum triglycerides level
        - ``s6`` (float): Blood sugar level

        Target:
        - Progression of diabetes one year after baseline (float)

    Notes
    -----
    The diabetes dataset is a subset of the larger diabetes dataset from scikit-learn.
    More details: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html

    Examples
    --------
    To get the processed data and target labels::

        data, target = shap.datasets.diabetes()


    """
    d = sklearn.datasets.load_diabetes()
    df = pd.DataFrame(data=d.data, columns=d.feature_names)
    target = d.target

    if n_points is not None:
        df = shap.utils.sample(df, n_points, random_state=0)
        target = shap.utils.sample(target, n_points, random_state=0)

    return df, target


def iris(display=False, n_points=None):
    """Return the classic Iris dataset in a convenient package.

    Parameters
    ----------
    display : bool
        If True, return the original feature matrix along with class labels (as strings). Default is False.
    - n_points : int, optional
        Number of data points to include. Default is None, including all data points.

    Returns
    -------
    Tuple of pandas DataFrame containing the feature matrix and either a numpy array representing the class labels or a list of class labels (if display is True).

    Notes
    -----
    - The dataset includes measurements of sepal length, sepal width, petal length, and petal width for three species of iris flowers.
    - Class labels are encoded as integers (0, 1, 2) representing the species (setosa, versicolor, virginica).
    - If display is True, class labels are returned as strings.

    Examples
    --------
    To get the feature matrix and class labels::

        features, labels = shap.datasets.iris()

    To get the feature matrix and class labels as strings::

        features, class_labels = shap.datasets.iris(display=True)

    """
    d = sklearn.datasets.load_iris()
    df = pd.DataFrame(data=d.data, columns=d.feature_names)
    target = d.target

    if n_points is not None:
        df = shap.utils.sample(df, n_points, random_state=0)
        target = shap.utils.sample(target, n_points, random_state=0)

    if display:
        return df, [d.target_names[v] for v in target]
    return df, target


def adult(display=False, n_points=None):
    """Return the Adult census data in a structured format.

    Parameters
    ----------
    display : bool, optional
        If True, return the raw data without target and redundant columns.
    n_points : int, optional
        Number of data points to sample. If provided, randomly samples the specified number of points.

    Returns
    -------
    If display is True:
        Tuple of pandas DataFrame containing the raw data without the 'Education', 'Target', and 'fnlwgt' columns,
        and a numpy array representing the 'Target' column.
    If display is False:
        Tuple of pandas DataFrame containing the processed data without the 'Target' and 'fnlwgt' columns,
        and a numpy array representing the 'Target' column.

    The data includes the following columns:
    - ``Age`` (float) : Age in years.
    - ``Workclass`` (category) : Type of employment.
    - ``fnlwgt`` (float) : Final weight; the number of units in the target population that the record represents.
    - ``Education`` (category) : Highest level of education achieved.
    - ``Education-Num`` (float) : Numeric representation of education level.
    - ``Marital Status`` (category) : Marital status of the individual.
    - ``Occupation`` (category) : Type of occupation.
    - ``Relationship`` (category) : Relationship status.
    - ``Race`` (category) : Ethnicity of the individual.
    - ``Sex`` (category) : Gender of the individual.
    - ``Capital Gain`` (float) : Capital gains recorded.
    - ``Capital Loss`` (float) : Capital losses recorded.
    - ``Hours per week`` (float) : Number of hours worked per week.
    - ``Country`` (category) : Country of origin.
    - ``Target`` (category) : Binary target variable indicating whether the individual earns more than 50K.

    Notes
    -----
    - The 'Education' column is redundant with 'Education-Num' and is dropped for simplicity.
    - The 'Target' column is converted to binary (True/False) where '>50K' is True and '<=50K' is False.
    - Certain categorical columns are encoded for numerical representation.

    Examples
    --------
    To get the processed data and target labels::

        data, target = shap.datasets.adult()

    To get the raw data for display::

        raw_data, target = shap.datasets.adult(display=True)

    """
    dtypes = [
        ("Age", "float32"), ("Workclass", "category"), ("fnlwgt", "float32"),
        ("Education", "category"), ("Education-Num", "float32"), ("Marital Status", "category"),
        ("Occupation", "category"), ("Relationship", "category"), ("Race", "category"),
        ("Sex", "category"), ("Capital Gain", "float32"), ("Capital Loss", "float32"),
        ("Hours per week", "float32"), ("Country", "category"), ("Target", "category")
    ]
    raw_data = pd.read_csv(
        cache(github_data_url + "adult.data"),
        names=[d[0] for d in dtypes],
        na_values="?",
        dtype=dict(dtypes)
    )

    if n_points is not None:
        raw_data = shap.utils.sample(raw_data, n_points, random_state=0)

    data = raw_data.drop(["Education"], axis=1)  # redundant with Education-Num
    filt_dtypes = list(filter(lambda x: x[0] not in ["Target", "Education"], dtypes))
    data["Target"] = data["Target"] == " >50K"
    rcode = {
        "Not-in-family": 0,
        "Unmarried": 1,
        "Other-relative": 2,
        "Own-child": 3,
        "Husband": 4,
        "Wife": 5
    }
    for k, dtype in filt_dtypes:
        if dtype == "category":
            if k == "Relationship":
                data[k] = np.array([rcode[v.strip()] for v in data[k]])
            else:
                data[k] = data[k].cat.codes

    if display:
        return raw_data.drop(["Education", "Target", "fnlwgt"], axis=1), data["Target"].values
    return data.drop(["Target", "fnlwgt"], axis=1), data["Target"].values


def nhanesi(display=False, n_points=None):
    """Return a nicely packaged version of NHANES I data with survival times as labels.

    Parameters
    ----------
    display : bool, optional
        If True, returns the features with a modified display. Default is False.
    n_points : int, optional
        Number of data points to sample. Default is None (returns the entire dataset).

    Returns
    -------
    If display is True, returns a modified version of the features for display along with survival times.
    If display is False, returns the original features along with survival times.

    Examples
    --------
    Usage example::

        features, survival_times = shap.datasets.nhanesi(display=True, n_points=100)

    """
    X = pd.read_csv(cache(github_data_url + "NHANESI_X.csv"), index_col=0)
    y = pd.read_csv(cache(github_data_url + "NHANESI_y.csv"), index_col=0)["y"]

    if n_points is not None:
        X = shap.utils.sample(X, n_points, random_state=0)
        y = shap.utils.sample(y, n_points, random_state=0)

    if display:
        X_display = X.copy()
        # X_display["sex_isFemale"] = ["Female" if v else "Male" for v in X["sex_isFemale"]]
        return X_display, np.array(y)
    return X, np.array(y)


def corrgroups60(n_points=1_000):
    """Correlated Groups 60

    A simulated dataset with tight correlations among distinct groups of features.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to generate. Default is 1,000.

    Returns
    -------
    Tuple of pandas DataFrame containing the features and a numpy array representing the target.

    Examples
    --------
    .. code-block:: python

        data, target = shap.datasets.corrgroups60()

    """
    # set a constant seed
    old_seed = np.random.seed()
    np.random.seed(0)

    # generate dataset with known correlation
    N, M = n_points, 60

    # set one coefficient from each group of 3 to 1
    beta = np.zeros(M)
    beta[0:30:3] = 1

    # build a correlation matrix with groups of 3 tightly correlated features
    C = np.eye(M)
    for i in range(0,30,3):
        C[i,i+1] = C[i+1,i] = 0.99
        C[i,i+2] = C[i+2,i] = 0.99
        C[i+1,i+2] = C[i+2,i+1] = 0.99
    def f(X):
        return np.matmul(X, beta)

    # Make sure the sample correlation is a perfect match
    X_start = np.random.randn(N, M)
    X_centered = X_start - X_start.mean(0)
    Sigma = np.matmul(X_centered.T, X_centered) / X_centered.shape[0]
    W = np.linalg.cholesky(np.linalg.inv(Sigma)).T
    X_white = np.matmul(X_centered, W.T)
    assert np.linalg.norm(np.corrcoef(np.matmul(X_centered, W.T).T) - np.eye(M)) < 1e-6 # ensure this decorrelates the data

    # create the final data
    X_final = np.matmul(X_white, np.linalg.cholesky(C).T)
    X = X_final
    y = f(X) + np.random.randn(N) * 1e-2

    # restore the previous numpy random seed
    np.random.seed(old_seed)

    return pd.DataFrame(X), y


def independentlinear60(n_points=1_000):
    """A simulated dataset with tight correlations among distinct groups of features.

    Parameters
    ----------
    n_points : int, optional
        Number of data points to generate. Default is 1,000.

    Returns
    -------
    Tuple of pandas DataFrame containing the feature matrix and a numpy array representing the labels.

    Notes
    -----
    - The dataset is generated with known correlations among distinct groups of features.
    - The labels are generated based on a linear function of the features with added random noise.

    Examples
    --------
    .. code-block:: python

        features, labels = shap.datasets.independentlinear60()
    """
    # set a constant seed
    old_seed = np.random.seed()
    np.random.seed(0)

    # generate dataset with known correlation
    N, M = n_points, 60

    # set one coefficient from each group of 3 to 1
    beta = np.zeros(M)
    beta[0:30:3] = 1
    def f(X):
        return np.matmul(X, beta)

    # Make sure the sample correlation is a perfect match
    X_start = np.random.randn(N, M)
    X = X_start - X_start.mean(0)
    y = f(X) + np.random.randn(N) * 1e-2

    # restore the previous numpy random seed
    np.random.seed(old_seed)

    return pd.DataFrame(X), y


def a1a(n_points=None):
    """
    Return a sparse dataset in scipy csr matrix format.
    Data Source: Scikit-learn datasets https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_svmlight_file.html

    Parameters
    ----------
    n_points : int or None, optional
        Number of data points to sample. If None, returns the entire dataset. Default is None.


    Returns
    -------
    - data : scipy.sparse.csr_matrix
        Sparse feature matrix.
    - target : numpy.ndarray
        Target labels.

    Examples
    --------
    .. code-block:: python

        # Usage example
        data, target = shap.datasets.a1a()

    """
    data, target = sklearn.datasets.load_svmlight_file(cache(github_data_url + 'a1a.svmlight'))

    if n_points is not None:
        data = shap.utils.sample(data, n_points, random_state=0)
        target = shap.utils.sample(target, n_points, random_state=0)

    return data, target

def rank():
    """Return ranking datasets from the LightGBM repository.

    Returns
    -------
    - x_train : scipy.sparse.csr_matrix
        Training feature matrix.
    - y_train : numpy.ndarray
        Training labels.
    - x_test : scipy.sparse.csr_matrix
        Testing feature matrix.
    - y_test : numpy.ndarray
        Testing labels.
    - q_train : numpy.ndarray
        Training query information.
    - q_test : numpy.ndarray
        Testing query information.

    Notes
    -----
    Data Source: LightGBM repository https://github.com/microsoft/LightGBM/tree/master/examples/lambdarank

    Examples
    --------
    .. code-block:: python

        # Usage example
        x_train, y_train, x_test, y_test, q_train, q_test = shap.datasets.rank()


    """
    rank_data_url = 'https://raw.githubusercontent.com/Microsoft/LightGBM/master/examples/lambdarank/'
    x_train, y_train = sklearn.datasets.load_svmlight_file(cache(rank_data_url + 'rank.train'))
    x_test, y_test = sklearn.datasets.load_svmlight_file(cache(rank_data_url + 'rank.test'))
    q_train = np.loadtxt(cache(rank_data_url + 'rank.train.query'))
    q_test = np.loadtxt(cache(rank_data_url + 'rank.test.query'))

    return x_train, y_train, x_test, y_test, q_train, q_test


def cache(url, file_name=None):
    """Loads a file from the URL and caches it locally."""
    if file_name is None:
        file_name = os.path.basename(url)
    data_dir = os.path.join(os.path.dirname(__file__), "cached_data")
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, file_name)
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)

    return file_path
