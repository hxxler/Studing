from math import ceil, exp, log
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys


np.random.seed(12)
bar_length = 50
count_of_image = 1


def ln_y(y: float, e: float):
    return e * log(y)


def entropy_loss(output: np.array, etalon: np.array) -> float:
    ln_y_v = np.vectorize(ln_y)
    error = 0
    error += np.sum(ln_y_v(output, etalon))
    error += np.sum(ln_y_v(1 - output, 1 - etalon))
    return -error


def mse_loss(output: np.array, etalon: np.array) -> float:
    return np.sum((output - etalon) ** 2) / 2


def relu(x: float) -> float:
    if x > 0:
        return x
    else:
        return 0.1 * x


def derivative_of_relu(x: float) -> float:
    if x > 0:
        return 1
    else:
        return 0.1


def sigmoid(x: float) -> float:
    if x > 500:
        return 1
    elif x < -150:
        return 0
    return 1 / (1 + exp(-x))


def derivative_of_sigmoid(x: float) -> float:
    return sigmoid(x) * (1 - sigmoid(x))


class Operation:
    size: tuple[int, int, int]

    def get_output(self, images: np.array) -> np.array:
        pass

    def get_error(self, in_images: np.array, errors: np.array) -> np.array:
        pass

    def learn(self, in_image: np.array, errors: np.array):
        pass


class Convolve(Operation):
    lr: float = 1

    def __init__(self, in_size: tuple[int, int, int], kernel_size: tuple[int, int, int], af, daf):
        self.size = in_size
        temp = [in_size[0]]
        for index in range(1, len(in_size)):
            temp.append(in_size[index] + 1 - kernel_size[index])

        self.out_size = tuple(temp)
        self.kernel_size = kernel_size

        self.af = np.vectorize(af)
        self.daf = np.vectorize(daf)

        self.kernel = (np.random.rand(kernel_size[0], kernel_size[1], kernel_size[2]) * 2 - 1) * 0.05

        self.biases = (np.random.rand(kernel_size[0], 1) * 2 - 1) * 0.05

        self.weights = np.zeros((self.size[0], self.size[1] * self.size[2] + 1, self.out_size[1] * self.out_size[2]))

        self.bool_matrix = np.zeros((self.size[0],  # для какой матрицы
                                     self.kernel_size[1],  # для какой строки в ядре
                                     self.kernel_size[2],  # для какого столбца в ядре
                                     self.size[1] * self.size[2] + 1,  # булевая матрица
                                     self.out_size[1] * self.out_size[2]), dtype=bool)  #

        shift = ((self.kernel_size[1] - 1) // 2, (self.kernel_size[2] - 1) // 2)

        for k in range(self.size[0]):

            for y in range(self.kernel_size[1]):
                for x in range(self.kernel_size[2]):
                    bool_kernel = np.zeros(self.kernel_size[1:])
                    bool_kernel[y, x] = True

                    for kernel_center_y in range(shift[0], self.out_size[1] - shift[0] + 2):
                        for kernel_center_x in range(shift[1], self.out_size[2] - shift[1] + 2):
                            image_for_kernel = np.zeros(self.size[1:], dtype=bool)

                            image_for_kernel[kernel_center_y - shift[0]: kernel_center_y + shift[0] + 1,
                                             kernel_center_x - shift[1]: kernel_center_x + shift[1] + 1] = bool_kernel

                            matrix_in_line = np.reshape(image_for_kernel,
                                                        (image_for_kernel.shape[0] * image_for_kernel.shape[1], 1))
                            matrix_in_line = np.append(matrix_in_line, np.array([[False]]), axis=0)

                            output_y = kernel_center_y - shift[0]
                            output_x = kernel_center_x - shift[1]

                            line_index = output_y * self.out_size[1] + output_x
                            self.bool_matrix[k, y, x, :, line_index] = matrix_in_line[:, 0]
        self.set_kernel(self.kernel)
        self.set_biases(self.biases)

    def set_kernel(self, kernel: np.array):
        self.weights = np.zeros((self.size[0], self.size[1] * self.size[2] + 1, self.out_size[1] * self.out_size[2]))
        self.kernel = np.copy(kernel)
        for k in range(self.kernel_size[0]):

            for y in range(self.kernel_size[1]):
                for x in range(self.kernel_size[2]):
                    self.weights[k, self.bool_matrix[k, y, x]] = kernel[k, y, x]

    def set_biases(self, biases: np.array):

        for k in range(self.kernel_size[0]):
            self.weights[k, -1, :] = biases[k, 0]

    def get_output(self, images: np.array) -> np.array:
        result = np.zeros(self.out_size)
        for k in range(self.size[0]):
            image = images[0]
            s = self.get_s(image, k)
            y = self.af(s)
            result[k] = np.reshape(y, self.out_size[1:])
        return result

    def get_s(self, image: np.array, k: int):

        x = np.reshape(image, (1, image.shape[0] * image.shape[1]))
        x = np.append(x, np.array([[-1]]), axis=1)
        return np.dot(x, self.weights[k])

    def get_error(self, in_images: np.array, errors: np.array) -> np.array:
        result = np.zeros(self.size)

        for k in range(self.size[0]):
            error = errors[k]
            image = in_images[k]

            s = self.get_s(image, k)

            error = np.reshape(error, (1, error.shape[0] * error.shape[1]))
            error_with_der = error * self.daf(s)

            result_error = np.dot(error_with_der, self.weights[k].T)[:, :-1]
            result[k] = np.reshape(result_error, self.size[1:])
        return result

    def learn(self, in_image: np.array, errors: np.array):

        for k in range(self.size[0]):
            image = in_image[k]
            error = errors[k]
            error_line = np.reshape(error, (1, error.shape[0] * error.shape[1]))
            x = np.reshape(image, (1, image.shape[0] * image.shape[1]))
            x = np.append(x, np.array([[-1]]), axis=1)
            error_with_der = self.daf(self.get_s(image, k)) * error_line

            delta_weights = self.lr / count_of_image * np.dot(error_with_der.T, x)

            self.biases[k, 0] -= np.sum(delta_weights[-1, :]) / delta_weights[-1, :].shape[0]
            self.weights[k, -1, :] = self.biases[k, 0]
            delta_weights = delta_weights.T

            for y in range(self.kernel_size[1]):
                for x in range(self.kernel_size[2]):
                    bool_matrix = self.bool_matrix[k, y, x]
                    total_error = np.sum(delta_weights[bool_matrix]) / delta_weights[bool_matrix].shape[0]
                    self.kernel[k, y, x] -= total_error

        self.set_kernel(self.kernel)


class MapConvert(Operation):

    def __init__(self, in_size: tuple[int, int, int], out_map_count: int, bool_matrix: np.array):
        self.size = in_size
        self.out_size = (out_map_count, self.size[1], self.size[2])
        self.bool_matrix = bool_matrix

    def get_output(self, images: np.array):
        result = np.zeros(self.out_size)
        for k in range(self.bool_matrix.shape[1]):
            temp = np.zeros(self.size[1:])
            for image_index in range(self.bool_matrix.shape[0]):
                if self.bool_matrix[image_index, k]:
                    temp += images[image_index]
                    result[k, :, :] += images[image_index]

            result[k] /= np.count_nonzero(self.bool_matrix[:, k])
        return result

    def get_error(self, in_images: np.array, errors: np.array) -> np.array:
        result = np.zeros(self.size)
        out_images_current = self.get_output(in_images)
        for k1 in range(out_images_current.shape[0]):
            bool_mask = self.bool_matrix[:, k1]
            error = errors[k1]
            result[bool_mask] += error
        return result


class Pooling(Operation):

    def __init__(self, in_size: tuple[int, int, int], kernel_size: tuple[int, int]):
        self.size = in_size
        self.out_size = (in_size[0], ceil(in_size[1] / kernel_size[0]), ceil(in_size[2] / kernel_size[1]))
        self.pool_size = kernel_size

    def get_output(self, images: np.array) -> np.array:
        if images.shape == self.size[1:]:
            images = np.array([images])
        result = np.zeros(self.out_size)
        for k in range(self.size[0]):
            image = images[k]
            for y in range(self.out_size[1]):
                for x in range(self.out_size[2]):
                    result[k, y, x] = np.max(image[y * self.pool_size[0]: (y + 1) * self.pool_size[0],
                                             x * self.pool_size[1]: (x + 1) * self.pool_size[1]])
        return result

    def get_error(self, in_images: np.array, errors: np.array) -> np.array:
        result = np.zeros(self.size)
        out_images_current = self.get_output(in_images)
        for k in range(self.size[0]):
            out_image_current = out_images_current[k]

            error = errors[k]
            image = in_images[k]

            for y in range(self.out_size[1]):
                for x in range(self.out_size[2]):
                    max_value = out_image_current[y, x]

                    mask = np.zeros(self.size[1:], dtype=bool)

                    mask[y * self.pool_size[0]: (y + 1) * self.pool_size[0],
                         x * self.pool_size[1]: (x + 1) * self.pool_size[1]] = True

                    temp = image[mask]
                    res = np.zeros_like(temp)
                    mask2 = temp >= max_value

                    index_of_true = np.argmax(mask2)

                    # Создаем новую маску, где только одно True значение
                    mask2 = np.zeros_like(mask2, dtype=bool)
                    mask2[index_of_true] = True

                    res[mask2] = error[y, x]

                    result[k, y * self.pool_size[0]: (y + 1) * self.pool_size[0],
                           x * self.pool_size[1]: (x + 1) * self.pool_size[1]] = np.reshape(res, self.pool_size)
        return result


class MLPLayer(Operation):
    lr: float = 1

    def __init__(self, in_size: tuple[int, int, int], out_count_of_neurons: int, af, daf):
        self.out_size = (in_size[0], 1, out_count_of_neurons)
        self.size = in_size
        self.weights = (np.random.rand(in_size[0] * in_size[1] * in_size[2] + 1, out_count_of_neurons) * 2 - 1) * 0.05
        self.af = np.vectorize(af)
        self.daf = np.vectorize(daf)

    def get_s(self, images: np.array):
        if images.shape == self.size[1:]:
            images = np.array([images])

        x = np.reshape(images, (1, images.shape[0] * images.shape[1] * images.shape[2]))
        x = np.append(x, np.array([[-1]]), axis=1)
        return np.dot(x, self.weights)

    def get_output(self, images: np.array) -> np.array:
        s = self.get_s(images)
        y = self.af(s)
        return y

    def get_error(self, in_images: np.array, errors: np.array) -> np.array:

        if in_images.shape == self.out_size[1:]:
            in_images = np.array([in_images])

        error_with_der = errors * self.daf(self.get_s(in_images))
        res = np.dot(errors, self.weights[:-1].T)  # так как используется кроссэнтропия то вместо производной берем 1
        return np.reshape(res, in_images.shape)

    def learn(self, images: np.array, errors: np.array):

        if images.shape == self.size[1:]:
            images = np.array([images])

        x = np.reshape(images, (1, images.shape[0] * images.shape[1] * images.shape[2]))
        x = np.append(x, np.array([[-1]]), axis=1)

        error_with_der_s = errors * self.daf(self.get_s(images))

        self.weights -= self.lr / count_of_image * np.dot(errors.T, x).T  # -//- вместо производной берем 1


class CNN:
    layers: list[MLPLayer | Convolve | MapConvert | Pooling]

    def __init__(self, layers: list[MLPLayer | MapConvert | Convolve | Pooling]):
        self.layers = layers

        self.etalons = np.zeros((0, 10))
        self.trainset = np.zeros((0, 28, 28))

    def fit(self, error=1.0e-1):

        epoch = 0

        current_error = self.get_error()
        try:
            while current_error > error:
                self.learn()
                current_error = self.get_error()
                epoch += 1
                if epoch < 100 or epoch % 100 == 0:
                    print(f"#{epoch:6d} - {current_error:.3e}")
        except:
            pass
        print(f"#{epoch:6d} - {current_error:.3e}")

    def learn(self):

        count_of_images = self.trainset.shape[0]
        for index in range(self.trainset.shape[0]):

            progress = index / count_of_images
            bar = '=' * int(progress * bar_length) + ' ' * (bar_length - int(progress * bar_length))
            percent = progress * 100
            sys.stdout.write('\r[%s] %d%%' % (bar, percent))
            sys.stdout.flush()

            image = self.trainset[index: index + 1]
            output = np.copy(image)
            etalon = self.etalons[index]

            in_out_list = [output]

            for layer in self.layers:
                in_out_list.append(layer.get_output(in_out_list[-1]))

            error = [in_out_list[-1] - etalon]

            for layer_index, layer in enumerate(self.layers[::-1]):
                error.append(layer.get_error(in_out_list[::-1][layer_index + 1], error[-1]))

            error = error[:-1]
            error = error[::-1]

            for layer_index, layer in enumerate(self.layers):
                layer.learn(in_out_list[layer_index], error[layer_index])
        sys.stdout.write('\r' + ' ' * (bar_length + 8) + '\r')
        sys.stdout.flush()

    def load_trainset(self, path: str):
        temp = np.genfromtxt(path, skip_header=True, delimiter=',')
        self.etalons = np.zeros((temp.shape[0], 1, 10))
        self.trainset = np.zeros((temp.shape[0], 28, 28))
        for j in range(temp[:, 0].shape[0]):
            self.etalons[j] = np.array([[0 if i != temp[j, 0] else 1 for i in range(10)]])
            self.trainset[j] = np.reshape(temp[j, 1:], (1, 28, 28)) / 255
        global count_of_image
        count_of_image = temp[:, 0].shape[0]

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.layers, f)

    def load(self, path: str):
        with open(path, 'rb') as f1:
            self.layers = pickle.load(f1)

    def test(self, path):
        temp = np.genfromtxt(path, skip_header=True, delimiter=',')

        etalons = np.zeros((temp.shape[0], 10))
        trainset = np.zeros((temp.shape[0], 28, 28))
        for j in range(temp[:, 0].shape[0]):
            etalons[j] = np.array([0 if i != temp[j, 0] else 1 for i in range(10)])
            trainset[j] = np.reshape(temp[j, 1:], (1, 28, 28)) / 255

        correct_count = 0

        for index in range(trainset.shape[0]):

            image = trainset[index: index + 1]
            output = np.copy(image)
            etalon = etalons[index]

            in_out_list = [output]

            for layer in self.layers:
                in_out_list.append(layer.get_output(in_out_list[-1]))

            result = in_out_list[-1]
            if np.argmax(etalon) == np.argmax(result):
                correct_count += 1
            print(np.argmax(etalon), np.argmax(result))
        print(f'Правильных ответов - {correct_count}, всего - {trainset.shape[0]}')

    def get_error(self) -> np.array:
        error = 0
        count_of_images = self.trainset.shape[0]
        for index, image in enumerate(self.trainset):
            progress = index / count_of_images
            bar = '=' * int(progress * bar_length) + ' ' * (bar_length - int(progress * bar_length))
            percent = progress * 100
            sys.stdout.write('\r[%s] %d%%' % (bar, percent))
            sys.stdout.flush()

            output = image
            etalon = self.etalons[index]
            for layer in self.layers:
                output = layer.get_output(np.reshape(output, layer.size))

            # error += np.sum((output - etalon) ** 2)  # MSE
            error += entropy_loss(output, etalon)  # Cross entropy

        sys.stdout.write('\r' + ' ' * (bar_length + 8) + '\r')
        sys.stdout.flush()
        error /= count_of_images
        return error

    def test_with_vizual(self, path):
        temp = np.genfromtxt(path, skip_header=True, delimiter=',')

        etalons = np.zeros((temp.shape[0], 10))
        trainset = np.zeros((temp.shape[0], 28, 28))
        for j in range(temp[:, 0].shape[0]):
            etalons[j] = np.array([0 if i != temp[j, 0] else 1 for i in range(10)])
            trainset[j] = np.reshape(temp[j, 1:], (1, 28, 28)) / 255

        for index in range(trainset.shape[0]):

            image = trainset[index: index + 1]
            output = np.copy(image)
            etalon = etalons[index]
            in_out_list = [output]

            for layer in self.layers:
                in_out_list.append(layer.get_output(in_out_list[-1]))

            result = np.copy(in_out_list[-1])
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(np.reshape(image, (28, 28)), cmap='gray', interpolation='nearest')
            for i in range(10):
                if i == np.argmax(etalon):
                    ax.text(28.5, i, f'{i} - {100 * result[0, i]:.2f}%', va='center', color='green')
                elif i == np.argmax(result):
                    ax.text(28.5, i, f'{i} - {100 * result[0, i]:.2f}%', va='center', color='blue')
                else:
                    ax.text(28.5, i, f'{i} - {100 * result[0, i]:.2f}%', va='center', )
            ax.axis('off')
            plt.show()

    def kernel_viz(self):
        for layer in self.layers:
            if isinstance(layer, Convolve):
                kernels = layer.kernel
                fig, axes = plt.subplots(5, 8, figsize=(10, 10))
                for i, ax in enumerate(axes.flat):
                    if i < kernels.shape[0]:
                        ax.imshow(kernels[i], cmap='gray')
                    ax.axis('off')
                plt.show()
