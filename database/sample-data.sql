-- Sample Bücher
INSERT INTO books (isbn, title, author, category, publication_year, total_copies, available_copies) VALUES
('9783446440814', 'Clean Code', 'Robert C. Martin', 'Informatik', 2008, 3, 2),
('9783836244893', 'Python Crashkurs', 'Eric Matthes', 'Informatik', 2019, 2, 1),
('9783499626418', 'Der Herr der Ringe', 'J.R.R. Tolkien', 'Fantasy', 1954, 5, 4),
('9783453031005', 'Per Anhalter durch die Galaxis', 'Douglas Adams', 'Science Fiction', 1979, 2, 2),
('9783596296323', 'Datenbanksysteme', 'Alfons Kemper', 'Informatik', 2015, 4, 3);

-- Sample Benutzer
INSERT INTO users (user_number, first_name, last_name, email, phone) VALUES
('STU001', 'Max', 'Mustermann', 'max.mustermann@dhbw.de', '+49123456789'),
('STU002', 'Anna', 'Schmidt', 'anna.schmidt@dhbw.de', '+49987654321'),
('STU003', 'Peter', 'Weber', 'peter.weber@dhbw.de', '+49555666777'),
('DOZ001', 'Prof. Dr.', 'Mueller', 'mueller@dhbw.de', '+49111222333');

-- Sample Ausleihvorgänge
INSERT INTO loans (book_isbn, user_number, loan_date, due_date, status) VALUES
('9783446440814', 'STU001', '2025-01-15', '2025-02-15', 'active'),
('9783836244893', 'STU002', '2025-01-10', '2025-02-10', 'returned'),
('9783499626418', 'STU001', '2025-01-20', '2025-02-20', 'active');

-- Update available_copies nach Ausleihen
UPDATE books SET available_copies = total_copies - (
    SELECT COUNT(*) FROM loans WHERE book_isbn = books.isbn AND status = 'active'
);