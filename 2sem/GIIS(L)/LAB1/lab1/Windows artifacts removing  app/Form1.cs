using System;
using System.Drawing;
using System.IO;
using System.Threading;
using System.Windows.Forms;

namespace Windows_artifacts_removing__app
{
    public partial class Form1 : Form

    {
        private void RemoveNoise(Bitmap image)
        {
            // Создаем копию изображения для работы с ней
            Bitmap resultImage = new Bitmap(image);

            // Получаем общее количество пикселей в изображении
            int totalPixels = (image.Width - 2) * (image.Height - 2);

            // Проходим по каждому пикселю изображения
            for (int y = 1; y < image.Height - 1; y++)
            {
                for (int x = 1; x < image.Width - 1; x++)
                {
                    // Создаем массив для хранения значений цвета в окрестности текущего пикселя
                    int[] redValues = new int[9];
                    int[] greenValues = new int[9];
                    int[] blueValues = new int[9];

                    // Заполняем массивы значениями цвета из окрестности текущего пикселя
                    int index = 0;
                    for (int dy = -1; dy <= 1; dy++)
                    {
                        for (int dx = -1; dx <= 1; dx++)
                        {
                            Color pixel = image.GetPixel(x + dx, y + dy);
                            redValues[index] = pixel.R;
                            greenValues[index] = pixel.G;
                            blueValues[index] = pixel.B;
                            index++;
                        }
                    }

                    // Сортируем массивы значений цвета
                    Array.Sort(redValues);
                    Array.Sort(greenValues);
                    Array.Sort(blueValues);

                    // Находим медианные значения цвета
                    int medianRed = redValues[4];
                    int medianGreen = greenValues[4];
                    int medianBlue = blueValues[4];

                    // Устанавливаем новый цвет для текущего пикселя
                    resultImage.SetPixel(x, y, Color.FromArgb(medianRed, medianGreen, medianBlue));

                    // Вычисляем текущий прогресс и обновляем прогресс-бар
                    int progress = (int)(((double)((y - 1) * (image.Width - 2) + (x - 1)) / totalPixels) * 100);
                    progressBar1.Value = progress;
                }
            }

            // Отображаем измененное изображение в pictureBox2
            pictureBox2.Image = resultImage;
            pictureBox2.SizeMode = PictureBoxSizeMode.Zoom;
            MessageBox.Show("Готово!");
            // Сбрасываем значение прогресса
            progressBar1.Value = 0;
        }

        void  AddNoise()
        {
            double probability = 0.03;
            // Создаем копию изображения для работы с ней
            Image image = pictureBox1.Image;
            Bitmap noisyImage = new Bitmap(image);

            // Получаем общее количество пикселей в изображении
            int totalPixels = image.Width * image.Height;

            // Вычисляем количество зашумленных пикселей на основе вероятности
            int numNoisyPixels = (int)(probability * totalPixels);

            // Создаем массив индексов зашумленных пикселей
            int[] noisyIndices = new int[numNoisyPixels];

            // Генерируем случайные индексы для зашумления
            Random rnd = new Random();
            for (int i = 0; i < numNoisyPixels; i++)
            {
                noisyIndices[i] = rnd.Next(0, totalPixels);
            }

            // Применяем шум к зашумленным пикселям
            for (int i = 0; i < numNoisyPixels; i++)
            {
                // Вычисляем координаты пикселя на изображении
                int x = noisyIndices[i] % image.Width;
                int y = noisyIndices[i] / image.Width;

                // Устанавливаем белый цвет (255) для зашумленного пикселя
                noisyImage.SetPixel(x, y, Color.FromArgb(255, 255, 255));
            }
            pictureBox2.SizeMode = PictureBoxSizeMode.Zoom;
            pictureBox2.Image = noisyImage;
            MessageBox.Show("Готово!");
           
        }




        bool isStartPic(Image img)
        {
            if(img == Properties.Resources.no_photo_icon)
            {
                return true;
            }

            else { return false; }
        }

            public Form1()
        {
           
            InitializeComponent();
            pictureBox3.BackColor = Color.Transparent;
            pictureBox4.BackColor = Color.Transparent;
            pictureBox5.BackColor = Color.Transparent;
            pictureBox6.BackColor = Color.Transparent;
            pictureBox7.BackColor = Color.Transparent;
  
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Image Files (*.jpg; *.jpeg; *.png; *.bmp)|*.jpg; *.jpeg; *.png; *.bmp";

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string selectedImagePath = openFileDialog.FileName;
                try
                {
                    Image image = Image.FromFile(selectedImagePath);
                    pictureBox1.Image = image;
                    pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("An error occurred while loading the image: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void pictureBox5_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = Properties.Resources.no_photo_icon;
            pictureBox1.SizeMode = PictureBoxSizeMode.CenterImage;
        }

        private void pictureBox4_Click(object sender, EventArgs e)
        {
            pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
            pictureBox1.Image = pictureBox2.Image;
            pictureBox2.Image = Properties.Resources.no_photo_icon;
        }

        private void pictureBox7_Click(object sender, EventArgs e)
        {
            pictureBox2.Image = Properties.Resources.no_photo_icon;
            pictureBox2.SizeMode = PictureBoxSizeMode.CenterImage;
        }

        private void pictureBox3_Click(object sender, EventArgs e)
        {
            if (pictureBox2.Image != null && !isStartPic(pictureBox2.Image))
            {
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "JPEG Image|*.jpg|PNG Image|*.png|Bitmap Image|*.bmp";
                saveFileDialog.Title = "Save an Image File";
                saveFileDialog.ShowDialog();

                if (saveFileDialog.FileName != "")
                {
                    try
                    {
                        pictureBox2.Image.Save(saveFileDialog.FileName);
                        MessageBox.Show("Картинка успешно сохранена.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Возникла ошибка при сохранении фото: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Нечего сохранять.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }


        private void button2_Click(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                AddNoise();
            }
            if (radioButton2.Checked)
            {
                RemoveNoise((Bitmap)pictureBox1.Image);
            }
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            ShowFullScreenImage(pictureBox2.Image);
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            ShowFullScreenImage(pictureBox1.Image);
        }

        private void ShowFullScreenImage(Image image)
        {
            // Создаем новое окно
            Form fullScreenForm = new Form();

            // Устанавливаем размеры окна в соответствии с размерами изображения
            fullScreenForm.ClientSize = image.Size;

            // Устанавливаем изображение в качестве фона окна
            PictureBox pictureBox = new PictureBox();
            pictureBox.Dock = DockStyle.Fill;
            pictureBox.Image = image;
            pictureBox.SizeMode = PictureBoxSizeMode.Zoom;
            fullScreenForm.Controls.Add(pictureBox);

            // Показываем окно
            fullScreenForm.ShowDialog();
        }
        private void RotatePictureBox()
        {
            int angle = 0;
            while (true)
            {
                angle++;
                if (angle >= 360)
                    angle = 0;

                if (InvokeRequired)
                {
                    BeginInvoke((MethodInvoker)delegate ()
                    {
                        pictureBox6.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                        pictureBox6.Invalidate();
                    });
                }
                else
                {
                    pictureBox6.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                    pictureBox6.Invalidate();
                }

                Thread.Sleep(10);
            }
        }
        private System.Windows.Forms.Timer rotationTimer;

        private void StartRotationTimer()
        {
            rotationTimer = new System.Windows.Forms.Timer();
            rotationTimer.Interval = 100; // Интервал в миллисекундах
            rotationTimer.Tick += RotatePictureBox;
            rotationTimer.Start();
        }

        private void StopRotationTimer()
        {
            if (rotationTimer != null)
            {
                rotationTimer.Stop();
                rotationTimer.Dispose();
                rotationTimer = null;
            }
        }

        private void RotatePictureBox(object sender, EventArgs e)
        {
            pictureBox6.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
            pictureBox6.Invalidate();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            StartRotationTimer();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            StopRotationTimer();
        }


        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox6_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
