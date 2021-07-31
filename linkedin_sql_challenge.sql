-- to get the reservation made by Customer whose lastname is Stephen
--since I'm not sure of the lastname spelling, trying to get list of similarly named customer's reservation list
select Reservations.Date, Reservations.PartySize, Customers.FirstName, Customers.LastName
from Reservations
join Customers on Customers.CustomerID = Reservations.CustomerID
where Customers.LastName like "Ste%" order by Reservations.date;

insert into Reservations (CustomerID, "Date", PartySize) values ((select CustomerID from Customers
where FirstName="Sam" and LastName="McAdams" and Email = "smac@rouxacademy.com"), "2020-07-14 18:00:00", 5);

insert into orders (CustomerID, OrderDate) values ( 70, CURRENT_TIMESTAMP);

insert into OrdersDishes (OrderID, DishID) values (1001, (select DishID from Dishes where Name="House Salad")),
(1001, (select DishID from Dishes where Name="Mini CheeseBurgers")),
(1001, (select DishID from Dishes where Name = "Tropical Blue Smoothie"));

-- two different querries to get the Total Cost for given Order
select sum(price) as "Total Order Cost" from Dishes where DishID in (select DishID from OrdersDishes where OrderID = 1001);
select sum(dishes.Price) as "Total Order Cost" from Dishes join OrdersDishes on OrdersDishes.DishID = Dishes.DishID where OrdersDishes.OrderID = 1001;

-- to find out which query takes less time as well as resource, can check the query plan. It will show the second command is better than first.
explain query plan select sum(dishes.Price) from Dishes join OrdersDishes on OrdersDishes.DishID = Dishes.DishID where OrdersDishes.OrderID = 1001;

-- setting favorite dish of a customer, so that we can use this info to celebrate his birthday
update Customers set FavoriteDish = (select DishID from Dishes where Name="Quinoa Salmon Salad") where CustomerID=42;

-- to get the top 5 customers who ordered the most so far
Select count(o.OrderID) as OrderCount, c.FirstName, c.LastName, c.Email from Orders o
join Customers c on c.CustomerID = o.CustomerID
group by o.CustomerID
order by OrderCount desc limit 5;

-- To get the number of available copies for book titled Dracula
select ((select count(Books.Title) from Books where Title = "Dracula")
-
(select count(Books.Title) from Loans
join Books on books.BookID = Loans.BookID
where Loans.ReturnedDate is NULL and Books.Title="Dracula")) as AvailableCopies;

-- insert new books into table
insert into Books (Title, Author, Published, Barcode) values ("Dracula", "Bram Stoker", 1897, "4819277482"),
("Gulliver's Travels", "Jonathan Swift", 1729, "4899254401");

-- insert new book loans for given book barcode to patron
insert into Loans (BookID, PatronID, LoanDate, DueDate) values
 ((select BookID from Books where Barcode = "4043822646"), (select PatronID from Patrons where Email = "jvaan@wisdompets.com"), "2020-08-25", "2020-09-08"),
  ((select BookID from Books where Barcode = "2855934983"), (select PatronID from Patrons where Email = "jvaan@wisdompets.com"), "2020-08-25", "2020-09-08");

--Get the list of books that are past given due date and not yet returned
select Books.Title, Books.Barcode, Patrons.FirstName, Patrons.LastName, Patrons.Email from Loans
 join Books on Loans.BookID = Books.BookID
 join Patrons on Loans.PatronID = Patrons.PatronID
 where Loans.DueDate = "2020-07-13" and Loans.ReturnedDate is Null;

-- to update returned date for books with given barcode
update Loans set ReturnedDate = "2020-07-05" where BookID in (select BookID FROM
  Books where Barcode in ("6435968624", "5677520613", "8730298424")) and ReturnedDate is null;

-- get the top 10 customers who boorowed least number of books from library
select count(Loans.BookID) as "Number of books loaned", Patrons.FirstName, Patrons.LastName, Patrons.Email from loans
  join Patrons on Loans.PatronID = Patrons.PatronID
  group by Loans.PatronID
  order by "Number of books loaned" ASC
  limit 10;

-- get the number of books available in library at present that were published in 1890
select count(distinct Books.BookID) as "BooksCount" from Books
  join Loans on Books.BookID = Loans.BookID
  where Books.Published = 1890 and Loans.ReturnedDate is not null;

-- get the list of book names along with barcode that were published after 1889 till 1900 that are in the library at the moment
select Books.Title, Books.Barcode, Books.Author, Books.Published from Books
 join Loans on Books.BookID = Loans.BookID
 where Books.Published > 1889 and Books.Published < 1900 and Loans.ReturnedDate is not null
 group by Books.BookID
 order by Books.Published;

select count(distinct Books.Title) as "PublishedBooksCount", Published from Books
 group by  Published
 order by "PublishedBooksCount" desc ;

select count(Books.Title) as "LoanedCount", Books.Title, Books.Author from Books
 join Loans on Books.BookID = Loans.BookID
 group by Books.Title
 order by LoanedCount DESC
 limit 5;
