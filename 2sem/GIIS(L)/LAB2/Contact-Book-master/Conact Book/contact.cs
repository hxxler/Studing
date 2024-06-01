

namespace Conact_Book
{
    internal class contact
    {
        public string Name { get; set; }
        public string Surname { get; set; }
        public string Address { get; set; }
        public string CellPhone { get; set; }


        public contact(string name, string surname, string address, string cellPhone)
        {
            Name = name;
            Surname = surname;
            Address = address;
            CellPhone = cellPhone;
        }
    }
}