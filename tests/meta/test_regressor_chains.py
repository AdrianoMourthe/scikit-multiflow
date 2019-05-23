from sklearn.datasets import make_regression
from skmultiflow.data import DataStream

from skmultiflow.meta import RegressorChain
from sklearn.linear_model import SGDRegressor

import numpy as np

import pytest


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_regressor_chains():
    X_reg, y_reg = make_regression(random_state=112, n_targets=3, n_samples=5150)
    stream = DataStream(X_reg, y_reg)
    stream.prepare_for_use()
    estimator = SGDRegressor(random_state=112, max_iter=10, tol=1e-3)
    learner = RegressorChain(base_estimator=estimator, random_state=112)

    X, y = stream.next_sample(150)
    learner.partial_fit(X, y)

    cnt = 0
    max_samples = 5000
    predictions = []
    true_labels = []
    wait_samples = 100

    while cnt < max_samples:
        X, y = stream.next_sample()
        # Test every n samples
        if (cnt % wait_samples == 0) and (cnt != 0):
            predictions.append(list(learner.predict(X)[0]))
            true_labels.append(y[0])

        learner.partial_fit(X, y)
        cnt += 1

    expected_predictions = [[-21.932581119953333, 1265662295936.5574, 7.5406725414072326e+22],
                            [-97.17297744582125, 5438576501559.791, -1.1370581201037737e+24],
                            [-60.06308622605051, 26421144038311.047, 1.3207650552720094e+25],
                            [-285.32687352244847, 8881551118262.033, -1.1322856827798374e+24],
                            [-115.80322693771457, -24997431307818.508, 2.85747306174037e+24],
                            [-12.184193815918672, 3510562166726.0283, -4.8590562435597834e+23],
                            [-94.99008392491476, 4794062761133.606, -1.8849188211946465e+24],
                            [66.35576182871232, -8147485653396.883, -7.492944375995595e+23],
                            [-52.145505628056995, -1013810481101.9043, -4.5310283013446384e+23],
                            [16.715060622072958, 562391244392.6193, 3.3789644409962397e+22],
                            [96.32219400190282, -20397346086007.85, 1.558245298240083e+24],
                            [-281.8168065846582, 118681520215938.52, 4.815807486956294e+25],
                            [-135.62679760307105, 20260866750185.832, 1.605753540523006e+24],
                            [0.07932047636460954, -708539394047.3298, -3.61482684929158e+22],
                            [-292.1646176261883, -11162615183157.55, -8.674643964570704e+23],
                            [-176.92746747754094, -29231218161585.13, 1.411600743825668e+24],
                            [-348.0498644784687, -100615393132365.25, 9.759683002046948e+23],
                            [30.948974669258675, -1199287119275.6328, 2.0866927007519847e+23],
                            [214.0020659569134, -24437173206276.543, 9.450880718880671e+23],
                            [153.98931593720746, 32675842205528.723, -1.7246747286222668e+24],
                            [99.39074016354951, -11385065116243.611, 1.0770253102805811e+24],
                            [127.81660709796127, 16929726964275.697, 7.14820947257164e+24],
                            [40.45505653639006, -14311951591200.725, -9.33193290094133e+23],
                            [117.52219878440611, 17952367624051.36, 4.5651719663788677e+23],
                            [75.53942801239991, -9231543699137.594, 3.2317133158453914e+24],
                            [31.795193207760704, -4084783706153.4004, -4.188095047309216e+23],
                            [68.5318978502461, 5735810247065.921, 1.7284713503779943e+24],
                            [65.18438567482129, -13298743450357.943, -1.4367047198923567e+24],
                            [-116.63952028337805, -344127767223.9295, 2.3925104169428623e+22],
                            [-76.81599010889556, 8711205431447.733, -1.1575305916673031e+24],
                            [263.1077717649874, 32146618104196.434, -7.240279466740839e+24],
                            [-94.07597099457413, -8216681977657.527, 2.3785728690780553e+24],
                            [-175.78429788635424, -368856885004.46, -5.7200993095587195e+22],
                            [59.648477499483285, -1752783828320.242, 2.1429953624557326e+23],
                            [71.68447202426032, -27151271800666.492, 9.367463190825582e+24],
                            [-189.96629636835922, -27090727476080.18, -3.8659883994544866e+24],
                            [-240.7920206809074, 15406047062899.537, 2.0609123388035027e+24],
                            [-105.80996634043589, -1518636404558.1646, -1.4166487855869706e+23],
                            [-164.02527753963858, -61386039046571.125, -2.179071650432624e+25],
                            [52.451759456657975, -988509747123.6125, -7.334899319683594e+22],
                            [68.37044139814127, -7434200892467.581, -7.535677215142279e+23],
                            [164.9457843624521, -9474550940989.51, -1.3512944635293625e+24],
                            [189.34401690407307, -14349556896444.508, 1.0732760415617274e+24],
                            [0.8944005517286119, 463945767759.78735, -1.9938544157612443e+22],
                            [71.7856433565235, -9804063257174.584, 4.7874862540754335e+23],
                            [-5.450502769025279, 281585481223.33276, 2.1974700575843552e+22],
                            [248.00190755589915, -81874135462745.58, -2.6532557110860303e+25],
                            [-113.86249490223707, 2634310697909.643, 1.580428629322546e+23],
                            [-35.92856878407447, -5410985463428.589, 2.522168862637753e+23]]

    print(predictions)
    assert np.allclose(np.array(predictions).all(), np.array(expected_predictions).all())
    assert type(learner.predict(X)) == np.ndarray

    # sklearn < .0.21
    expected_info_0 = "RegressorChain(base_estimator=SGDRegressor(alpha=0.0001, average=False, early_stopping=False, " \
                      "epsilon=0.1,\n" \
                      "       eta0=0.01, fit_intercept=True, l1_ratio=0.15,\n" \
                      "       learning_rate='invscaling', loss='squared_loss', max_iter=10,\n" \
                      "       n_iter=None, n_iter_no_change=5, penalty='l2', power_t=0.25,\n" \
                      "       random_state=112, shuffle=True, tol=0.001, validation_fraction=0.1,\n" \
                      "       verbose=0, warm_start=False),\n" \
                      "               order=None, random_state=112)"
    # sklearn >= .0.21
    expected_info_1 = "RegressorChain(base_estimator=SGDRegressor(alpha=0.0001, average=False, early_stopping=False, " \
                      "epsilon=0.1,\n" \
                      "             eta0=0.01, fit_intercept=True, l1_ratio=0.15,\n" \
                      "             learning_rate='invscaling', loss='squared_loss', max_iter=10,\n" \
                      "             n_iter_no_change=5, penalty='l2', power_t=0.25, random_state=112,\n" \
                      "             shuffle=True, tol=0.001, validation_fraction=0.1, verbose=0,\n" \
                      "             warm_start=False),\n" \
                      "               order=None, random_state=112)"

    assert learner.get_info() == expected_info_0 or learner.get_info() == expected_info_1