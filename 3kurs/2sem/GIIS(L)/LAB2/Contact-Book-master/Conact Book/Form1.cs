using OfficeOpenXml;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;
using System.Linq;
using System.Threading;
using System.Windows.Forms;



namespace Conact_Book
{
   
    public partial class Form1 : Form
    {
        private int currentRow = 0;
        private ExcelPackage package = null;
        private List<contact> contacts = new List<contact>();
        private void addTestContacts()
        {
            contact Andre = new contact("John", "Doe", "123 Main St", "555-1234");
        }

        private void LoadExcelData(string filePath)
        {
            try
            {
                if (!File.Exists(filePath))
                {
                    MessageBox.Show("Файл не найден.");
                    return;
                }

                // Обновляем текст label5 с названием выбранного файла
                label5.Text = Path.GetFileName(filePath);

                // Открываем файл Excel для чтения
                FileInfo fileInfo = new FileInfo(filePath);
                package = new ExcelPackage(fileInfo); // Убираем using
                ExcelWorksheet worksheet = package.Workbook.Worksheets[0];
                int rowCount = worksheet.Dimension.Rows;
                int colCount = worksheet.Dimension.Columns;

                // Показываем первую строку данных по умолчанию
                currentRow = 1;
                DisplayCurrentRowData(worksheet);
                next_Button.Enabled = rowCount > 1;
           
            }
            catch (Exception ex)
            {
                MessageBox.Show("Произошла ошибка с загрузкой Excel файла: " + ex.Message);
            }
        }


        private void DisplayCurrentRowData(ExcelWorksheet worksheet)
        {
            // Проверяем, что currentRow находится в допустимом диапазоне строк
            if (currentRow >= 1 && currentRow <= worksheet.Dimension.Rows)
            {
                nameTextBox.Text = worksheet.Cells[currentRow, 1].Value?.ToString();
                surnameTextBox.Text = worksheet.Cells[currentRow, 2].Value?.ToString();
                cellPhoneTextBox.Text = worksheet.Cells[currentRow, 3].Value?.ToString();
                addressTextBox.Text = worksheet.Cells[currentRow, 4].Value?.ToString();
                progressLabel.ForeColor = Color.Goldenrod;
                progressLabel.Text = $"{currentRow}/{worksheet.Dimension.Rows}";
                progressLabel.Refresh(); // или progressLabel.Invalidate();

            }
            else
            {
                // Если currentRow находится вне допустимого диапазона строк, выводим сообщение об ошибке
                MessageBox.Show("Текущая строка выходит за пределы диапазона.");
            }
        }


        private void highLightButtons()
        {
            List<PictureBox> list = new List<PictureBox>();
            list.Add(add_button);
            list.Add(delete_button);
            list.Add(export_Button);
            list.Add(search_Button);
            list.Add(Load_button);
            list.Add(save_Button);
            list.Add(next_Button);
            list.Add(previous_button);
            foreach (PictureBox item in list)
            {
                HighlightPictureBox(item);
            }
        }
        private void HighlightPictureBox(PictureBox pictureBox)
        {
            // Устанавливаем цвет подсветки
            Color highlightColor = Color.LightGray;

            // Обработчик события MouseEnter
            pictureBox.MouseEnter += (sender, e) =>
            {
                pictureBox.BackColor = highlightColor;
            };

            // Обработчик события MouseLeave
            pictureBox.MouseLeave += (sender, e) =>
            {
                pictureBox.BackColor = Color.Transparent; // Сбрасываем цвет подсветки при уходе мыши
            };
        }

     

        public Form1()
        {
            InitializeComponent();
            highLightButtons();
            /*addLabels();*/
        }

        private void add_button_Click(object sender, EventArgs e)
        {
            bool contactExists = false;
            if (package == null)
            {
                // Проверяем, существует ли контакт с такими же значениями в списке contacts
                foreach (contact existingContact in contacts)
                {
                    if (existingContact.Name == nameTextBox.Text &&
                        existingContact.Surname == surnameTextBox.Text &&
                        existingContact.Address == addressTextBox.Text && // Поменяли местами адрес и номер телефона
                        existingContact.CellPhone == cellPhoneTextBox.Text)
                    {
                        contactExists = true;
                        break;
                    }
                }

                // Если контакт уже существует, выводим сообщение об этом
                if (contactExists)
                {
                    MessageBox.Show("Контакт с такими же значениями уже существует.");
                    return;
                }

                // Если файл Excel не загружен и контакт не существует, добавляем контакт в список contacts
                contact newContact = new contact(nameTextBox.Text, surnameTextBox.Text, cellPhoneTextBox.Text, addressTextBox.Text); // Поменяли местами адрес и номер телефона
                contacts.Add(newContact);
                currentRow = contacts.Count - 1;
                DisplayCurrentContactData();
                MessageBox.Show("Новый контакт успешно добавлен в локальный лист.");
            }
            else
            {
                // Проверяем, существует ли контакт с такими же значениями в файле Excel
                ExcelWorksheet worksheet = package.Workbook.Worksheets[0];
                int lastRow = worksheet.Dimension.End.Row;

                for (int row = 1; row <= lastRow; row++)
                {
                    if (worksheet.Cells[row, 1].Value?.ToString() == nameTextBox.Text &&
                        worksheet.Cells[row, 2].Value?.ToString() == surnameTextBox.Text &&
                        worksheet.Cells[row, 4].Value?.ToString() == addressTextBox.Text && // Поменяли местами адрес и номер телефона
                        worksheet.Cells[row, 3].Value?.ToString() == cellPhoneTextBox.Text)
                    {
                        contactExists = true;
                        break;
                    }
                }

                // Если контакт уже существует, выводим сообщение об этом
                if (contactExists)
                {
                    MessageBox.Show("Контакт с такими же значениями уже существует в Excel файле.");
                    return;
                }

                // Если файл Excel загружен и контакт не существует, добавляем контакт в файл Excel
                worksheet.Cells[lastRow + 1, 1].Value = nameTextBox.Text;
                worksheet.Cells[lastRow + 1, 2].Value = surnameTextBox.Text;
                worksheet.Cells[lastRow + 1, 4].Value = addressTextBox.Text; // Поменяли местами адрес и номер телефона
                worksheet.Cells[lastRow + 1, 3].Value = cellPhoneTextBox.Text;

                MessageBox.Show("Новый контакт успешно добавлен в Excel файл.");
            }
        }



        private void delete_button_Click(object sender, EventArgs e)
        {
            if (package != null)
            {
                if (MessageBox.Show("Вы уверены, что хотите удалить выбранный контакт из Excel файла?", "Подтверждение удаления", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    ExcelWorksheet worksheet = package.Workbook.Worksheets[0];
                    int selectedRow = currentRow;

                    worksheet.DeleteRow(selectedRow);

                    MessageBox.Show("Контакт успешно удален из Excel файла.");
                }
            }

            if (currentRow >= 0 && currentRow < contacts.Count)
            {
                DialogResult result = MessageBox.Show("Вы уверены, что хотите удалить выбранный контакт из локального списка?", "Подтверждение удаления", MessageBoxButtons.YesNo);
                if (result == DialogResult.Yes)
                {
                    contacts.RemoveAt(currentRow);
                    MessageBox.Show("Контакт успешно удален из локального списка.");
                    currentRow = Math.Max(0, currentRow - 1); // Уменьшаем currentRow, чтобы он остался в пределах списка после удаления
                    DisplayCurrentContactData(); // Обновляем отображение данных
                }
            }
            else
            {
                MessageBox.Show("Выберите контакт для удаления.");
            }
        }



        private void edit_button_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Чтобы отредактировать контакт, обновите информацию в полях старыми данными.");
        }


        private void search_Button_Click(object sender, EventArgs e)
        {
            string searchName = Microsoft.VisualBasic.Interaction.InputBox("Введите имя для поиска:", "Поиск контактов", "");

            if (!string.IsNullOrWhiteSpace(searchName))
            {
                if (package != null)
                {
                    SearchInExcel(searchName);
                }
                else
                {
                    var foundContacts = contacts.Where(contact => contact.Name.Contains(searchName) || contact.Surname.Contains(searchName)).ToList();


                    if (foundContacts.Any())
                    {
                        string message = "Найден контакт:\n\n";
                        foreach (var contact in foundContacts)
                        {
                            message += $"Имя: {contact.Name}\nФамилия: {contact.Surname}\nТелефон: {contact.CellPhone}\nАдрес: {contact.Address}\n\n";
                        }
                        MessageBox.Show(message, "Найденный контакт");
                    }
                    else
                    {
                        MessageBox.Show($"Не найден контакт с именем '{searchName}'.", "Результаты поиска");
                    }
                }
               
            }
            else
            {
                MessageBox.Show("Введите имя контакта для поиска.", "Поиск контактов");
            }
        }

        private void SearchInExcel(string searchName)
        {
            if (package != null)
            {
                ExcelWorksheet worksheet = package.Workbook.Worksheets[0];
                int rowCount = worksheet.Dimension.Rows;
                int colCount = worksheet.Dimension.Columns;
                bool contactFound = false;

                for (int row = 2; row <= rowCount; row++)
                {
                    for (int col = 1; col <= colCount; col++)
                    {
                        string cellValue = worksheet.Cells[row, col].Value?.ToString();

                        if (!string.IsNullOrEmpty(cellValue) && cellValue.IndexOf(searchName, StringComparison.OrdinalIgnoreCase) >= 0)
                        {
                            // Отображаем найденный контакт в группе боксе
                            currentRow = row;
                            DisplayCurrentRowData(worksheet);
                            contactFound = true;
                            break;
                        }
                    }

                    if (contactFound)
                    {
                        break;
                    }
                }

                if (!contactFound)
                {
                    MessageBox.Show($"Не найден контакт с именем '{searchName}'.", "Результаты поиска");
                }
            }
            else
            {
                MessageBox.Show("Сначала загрузите Excel файл.");
            }
        }



        private void Load_button_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Excel Files (*.xlsx)|*.xlsx|All files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                string selectedFilePath = openFileDialog.FileName;
                LoadExcelData(selectedFilePath);
            }
        }

        private void save_Button_Click(object sender, EventArgs e)
        {
            if (package == null)
            {
                MessageBox.Show("Сначала откройте Excel файл");
            }
            else
            {
                try
                {
                    package.Save();
                    MessageBox.Show("Файл сохранен успешно.");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Произошла ошибка: " + ex.Message);
                }
            }

        }

        private void CreateExcelFile(string filePath)
        {
            FileInfo newFile = new FileInfo(filePath);
            using (ExcelPackage newPackage = new ExcelPackage(newFile))
            {
                ExcelWorksheet worksheet = newPackage.Workbook.Worksheets.Add("Contacts");

                worksheet.Cells[1, 1].Value = "Имя";
                worksheet.Cells[1, 2].Value = "Фамилия";
                worksheet.Cells[1, 3].Value = "Телефон";
                worksheet.Cells[1, 4].Value = "Адрес";

                int row = 2;
                foreach (var contact in contacts)
                {
                    worksheet.Cells[row, 1].Value = contact.Name;
                    worksheet.Cells[row, 2].Value = contact.Surname;
                    worksheet.Cells[row, 3].Value = contact.CellPhone;
                    worksheet.Cells[row, 4].Value = contact.Address;
                    row++;
                }

                newPackage.Save();
            }
        }





        private void previous_button_Click(object sender, EventArgs e)
        {
            if (package != null)
            {
         
                if (currentRow > 1)
                {
                    currentRow--;
                    ExcelWorksheet worksheet = package.Workbook.Worksheets[0];
                    DisplayCurrentRowData(worksheet);

              
                    next_Button.Enabled = currentRow < worksheet.Dimension.Rows;

             
                }
                else
                {
                    MessageBox.Show("Достигнут первый контакт списка.");
                }
            }
            else 
            {
                if (currentRow > 0)
                {
                    currentRow--;
                    DisplayCurrentContactData();

      
                    next_Button.Enabled = true;
                }
                else
                {
                    MessageBox.Show("Достигнут первый контакт списка.");
                }
            }
        }


        private void next_Button_Click(object sender, EventArgs e)
        {

            if (package != null)
            {
                ExcelWorksheet worksheet = package.Workbook.Worksheets[0];

  
                if (currentRow < worksheet.Dimension.Rows)
                {
                    currentRow++;

                    DisplayCurrentRowData(worksheet);
                }
                else
                {
                    MessageBox.Show("Достигнут последний контакт списка.");
                }
            }
            else 
            {
          
                if (contacts.Count > 0 && currentRow < contacts.Count - 1)
                {
                    currentRow++;

              
                    DisplayCurrentContactData();
                }
                else
                {
                    MessageBox.Show("Достигнут последний контакт списка.");
                }
            }
        }

        private void DisplayCurrentContactData()
        {
            if (contacts.Count > 0 && currentRow >= 0 && currentRow < contacts.Count)
            {
                nameTextBox.Text = contacts[currentRow].Name;
                surnameTextBox.Text = contacts[currentRow].Surname;
                cellPhoneTextBox.Text = contacts[currentRow].CellPhone;
                addressTextBox.Text = contacts[currentRow].Address;
                progressLabel.ForeColor = Color.Goldenrod;
                progressLabel.Text = $"{currentRow + 1}/{contacts.Count}";
                progressLabel.Refresh(); // или progressLabel.Invalidate();
            }
        }


        private void SaveVCFFile(string filePath)
        {
            try
            {
                // Используем конструктор StreamWriter с указанием кодировки
                using (StreamWriter writer = new StreamWriter(filePath, false, Encoding.GetEncoding("ISO-8859-1")))
                {
                    foreach (contact contact in contacts)
                    {
                        writer.WriteLine("BEGIN:VCARD");
                        writer.WriteLine("VERSION:2.1");
                        writer.WriteLine($"N:{contact.Surname};{contact.Name}");
                        writer.WriteLine($"FN:{contact.Name} {contact.Surname}");
                        writer.WriteLine($"TEL;TYPE=CELL:{contact.CellPhone}");
                        writer.WriteLine($"ADR:{contact.Address}");
                        writer.WriteLine("END:VCARD");
                    }
                }
                MessageBox.Show("Contacts saved successfully to the new VCF file.");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error saving contacts: {ex.Message}");
            }
        }

        private void export_Button_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "VCF Files (*.vcf)|*.vcf|All files (*.*)|*.*"; // Убираем формат Excel
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                string saveFilePath = saveFileDialog.FileName;
                SaveVCFFile(saveFilePath);
            }
        }
    



    private void label1_Click(object sender, EventArgs e)
        {

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
                        pictureBox3.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                        pictureBox3.Invalidate();
                    });
                }
                else
                {
                    pictureBox3.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                    pictureBox3.Invalidate();
                }

                Thread.Sleep(10);
            }
        }
        private System.Windows.Forms.Timer rotationTimer;

        private void StartRotationTimer()
        {
            rotationTimer = new System.Windows.Forms.Timer();
            rotationTimer.Interval = 250; // Интервал в миллисекундах
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
            pictureBox3.Image.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
            pictureBox3.Invalidate();
        }
        private void pictureBox3_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            StartRotationTimer();
        }

        private void nameTextBox_TextChanged(object sender, EventArgs e)
        {

        }

        private void pictureBox4_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void addressTextBox_TextChanged(object sender, EventArgs e)
        {

        }

        private void cellPhoneTextBox_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
