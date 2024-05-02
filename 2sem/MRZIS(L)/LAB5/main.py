from CNN import *


def learn():

    ae: list[CNNAutoencoder] = [CNNAutoencoder([
                                    Convolve((1, 28, 28), (1, 5, 5), relu, derivative_of_relu),

                                    MLPLayer((1, 24, 24), 100, relu, derivative_of_relu),
                                    UnMLPLayer(100, (1, 24, 24), relu, derivative_of_relu),

                                    UnConvolve((1, 24, 24), (1, 5, 5), sigmoid, derivative_of_sigmoid),
                                ]) for _ in range(10)]
    error = 135
    for i in range(10):
        ae[i].load_trainset(f'datasets/{i}.csv')

        # ae[i].load(f'weights/{i}.wbc')       # загружаем предобученные веса
        ae[i].fit(error)  # обучаем до ошибки
        ae[i].save(f'weights/{i}.wbc')  # сохраняем веса


def test():
    ae: list[CNNAutoencoder] = [CNNAutoencoder([
        Convolve((1, 28, 28), (1, 5, 5), relu, derivative_of_relu),

        MLPLayer((1, 24, 24), 100, relu, derivative_of_relu),
        UnMLPLayer(100, (1, 24, 24), relu, derivative_of_relu),

        UnConvolve((1, 24, 24), (1, 5, 5), sigmoid, derivative_of_sigmoid),
    ]) for _ in range(10)]

    for i in range(10):
        ae[i].load(f'weights/{i}.wbc')
        pass

    temp = np.genfromtxt('datasets/mnist_test.csv', skip_header=True, delimiter=',')
    n = temp.shape[0]
    images = np.reshape(temp[:, 1:], (n, 28, 28)) / 255
    etalons = temp[:, 0]
    corrected_answer = 0
    for k in range(n):
        errors = np.zeros(tuple([10]))
        outputs = np.zeros((10, 28, 28))
        image = images[k]

        for i in range(10):
            out = ae[i].get_output(image)

            error = entropy_loss(out, image)
            outputs[i] = out
            errors[i] = error

        index = np.argmin(errors)
        is_viz = not True

        if is_viz:
            fig, axes = plt.subplots(3, 4, figsize=(12, 9))

            for i, ax in enumerate(axes.flat):
                if i < 10:
                    ax.imshow(outputs[i], cmap='gray')
                    ax.set_axis_off()  # Убираем оси координат
                elif i == 10:
                    ax.imshow(image, cmap='gray')
                    ax.set_axis_off()  # Убираем оси координат
                else:

                    for z in range(10):
                        color = 'black'
                        if z == index:
                            color = 'blue'
                        if z == int(etalons[k]):
                            color = 'green'
                        ax.text(0.5, 1 - 0.1*z, f'#{z} {errors[z]}', horizontalalignment='center',
                                verticalalignment='center', fontsize=10, color=color)
                        ax.set_axis_off()
            plt.show()

        if index == int(etalons[k]):
            corrected_answer += 1
        print(index, int(etalons[k]))
    print(f'Правильно {corrected_answer} из {etalons.shape[0]}')


def main():
    is_learn = False

    if is_learn:
        learn()
    else:
        test()


if __name__ == '__main__':
    main()
