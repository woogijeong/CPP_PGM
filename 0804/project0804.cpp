//계산기
/*

#include <iostream>
using namespace std;

int main() {
    double result, num;
    char op;

    cout << "초기값 입력: ";
    cin >> result;

    while (true) {
        cout << "\n현재 값: " << result << endl;
        cout << "연산 입력 (+ - * /, 종료:q): ";
        cin >> op;

        if (op == 'q' || op == 'Q') {
            break;
        }

        cout << "숫자 입력: ";
        cin >> num;

        switch (op) {
        case '+':
            result += num;
            break;

        case '-':
            result -= num;
            break;

        case '*':
            result *= num;
            break;

        case '/':
            if (num != 0)
                result /= num;
            else
                cout << "0으로 나눌 수 없습니다." << endl;
            break;

        default:
            cout << "잘못된 연산자입니다." << endl;
        }

        cout << "결과 = " << result << endl;
    }

    cout << "\n최종 결과 = " << result << endl;
    cout << "계산기를 종료합니다." << endl;

    return 0;
}

*/


// 도서관리 프로그램//

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <fstream>
#include <sstream>

// ==========================================
// 1. 도서 (Book) 클래스
// ==========================================
class Book {
private:
    int id;
    std::string title;
    std::string author;
    bool isBorrowed;

public:
    Book(int id, const std::string& title, const std::string& author, bool isBorrowed = false)
        : id(id), title(title), author(author), isBorrowed(isBorrowed) {
    }

    int getId() const { return id; }
    std::string getTitle() const { return title; }
    std::string getAuthor() const { return author; }
    bool getIsBorrowed() const { return isBorrowed; }

    void setBorrowed(bool status) { isBorrowed = status; }

    void printInfo() const {
        std::cout << "[" << id << "] " << title << " (저자: " << author << ") - "
            << (isBorrowed ? "대출 중" : "대출 가능") << "\n";
    }

    std::string toCSV() const {
        return std::to_string(id) + "," + title + "," + author + "," + (isBorrowed ? "1" : "0");
    }

    static std::shared_ptr<Book> fromCSV(const std::string& line) {
        std::stringstream ss(line);
        std::string idStr, title, author, borrowedStr;

        if (std::getline(ss, idStr, ',') &&
            std::getline(ss, title, ',') &&
            std::getline(ss, author, ',') &&
            std::getline(ss, borrowedStr, ',')) {
            int id = std::stoi(idStr);
            bool isBorrowed = (borrowedStr == "1");
            return std::make_shared<Book>(id, title, author, isBorrowed);
        }
        return nullptr;
    }
};

// ==========================================
// 2. 회원 (User) 클래스
// ==========================================
class User {
private:
    int userId;
    std::string name;

public:
    User(int id, const std::string& name) : userId(id), name(name) {}

    int getUserId() const { return userId; }
    std::string getName() const { return name; }

    void printInfo() const {
        std::cout << "회원 ID: " << userId << " | 이름: " << name << "\n";
    }

    std::string toCSV() const {
        return std::to_string(userId) + "," + name;
    }

    static User fromCSV(const std::string& line) {
        std::stringstream ss(line);
        std::string idStr, name;

        if (std::getline(ss, idStr, ',') && std::getline(ss, name, ',')) {
            return User(std::stoi(idStr), name);
        }
        return User(0, "");
    }
};

// ==========================================
// 3. 도서관 관리 (LibraryManager) 클래스
// ==========================================
class LibraryManager {
private:
    std::vector<std::shared_ptr<Book>> books;
    std::vector<User> users;
    int nextBookId = 1;
    int nextUserId = 101;

    const std::string bookFileName = "books.txt";
    const std::string userFileName = "users.txt";

public:
    LibraryManager() {
        loadData();
    }

    ~LibraryManager() {
        saveData();
    }

    void saveData() const {
        std::ofstream bookFile(bookFileName);
        if (bookFile.is_open()) {
            for (const auto& book : books) {
                bookFile << book->toCSV() << "\n";
            }
            bookFile.close();
        }

        std::ofstream userFile(userFileName);
        if (userFile.is_open()) {
            for (const auto& user : users) {
                userFile << user.toCSV() << "\n";
            }
            userFile.close();
        }
        std::cout << ">> 데이터가 파일에 저장되었습니다.\n";
    }

    void loadData() {
        books.clear();
        users.clear();

        std::ifstream bookFile(bookFileName);
        if (bookFile.is_open()) {
            std::string line;
            int maxId = 0;
            while (std::getline(bookFile, line)) {
                if (line.empty()) continue;
                auto book = Book::fromCSV(line);
                if (book) {
                    books.push_back(book);
                    if (book->getId() > maxId) maxId = book->getId();
                }
            }
            bookFile.close();
            nextBookId = maxId + 1;
        }

        std::ifstream userFile(userFileName);
        if (userFile.is_open()) {
            std::string line;
            int maxId = 100;
            while (std::getline(userFile, line)) {
                if (line.empty()) continue;
                User user = User::fromCSV(line);
                if (user.getUserId() != 0) {
                    users.push_back(user);
                    if (user.getUserId() > maxId) maxId = user.getUserId();
                }
            }
            userFile.close();
            nextUserId = maxId + 1;
        }

        if (books.empty() && users.empty()) {
            addBook("C++ 프로그래밍", "비야네 스트롭스트룹");
            addBook("클린 코드", "로버트 C. 마틴");
            addUser("홍길동");
            saveData();
        }
    }

    // --- C R U D 기능 ---

    // 도서 등록
    void addBook(const std::string& title, const std::string& author) {
        books.push_back(std::make_shared<Book>(nextBookId++, title, author));
        std::cout << ">> 도서가 성공적으로 등록되었습니다. (도서 ID: " << nextBookId - 1 << ")\n";
    }

    // 도서 삭제 (신규 기능)
    void removeBook(int bookId) {
        auto it = std::find_if(books.begin(), books.end(), [bookId](const std::shared_ptr<Book>& b) {
            return b->getId() == bookId;
            });

        if (it == books.end()) {
            std::cout << ">> 오류: 삭제할 도서 ID(" << bookId << ")를 찾을 수 없습니다.\n";
            return;
        }

        if ((*it)->getIsBorrowed()) {
            std::cout << ">> 오류: 대출 중인 도서는 삭제할 수 없습니다. 반납 후 다시 시도해주세요.\n";
            return;
        }

        std::string title = (*it)->getTitle();
        books.erase(it);
        std::cout << ">> '" << title << "' (ID: " << bookId << ") 도서가 삭제되었습니다.\n";
    }

    // 회원 등록
    void addUser(const std::string& name) {
        users.push_back(User(nextUserId++, name));
        std::cout << ">> 회원이 성공적으로 등록되었습니다. (회원 ID: " << nextUserId - 1 << ")\n";
    }

    // 회원 삭제 (신규 기능)
    void removeUser(int userId) {
        auto it = std::find_if(users.begin(), users.end(), [userId](const User& u) {
            return u.getUserId() == userId;
            });

        if (it == users.end()) {
            std::cout << ">> 오류: 삭제할 회원 ID(" << userId << ")를 찾을 수 없습니다.\n";
            return;
        }

        std::string name = it->getName();
        users.erase(it);
        std::cout << ">> 회원 '" << name << "' (ID: " << userId << ")이(가) 삭제되었습니다.\n";
    }

    // 조회 및 검색
    void showAllBooks() const {
        std::cout << "\n--- [ 도서 목록 ] ---\n";
        if (books.empty()) {
            std::cout << "등록된 도서가 없습니다.\n";
            return;
        }
        for (const auto& book : books) {
            book->printInfo();
        }
    }

    void showAllUsers() const {
        std::cout << "\n--- [ 회원 목록 ] ---\n";
        if (users.empty()) {
            std::cout << "등록된 회원이 없습니다.\n";
            return;
        }
        for (const auto& user : users) {
            user.printInfo();
        }
    }

    void searchBook(const std::string& keyword) const {
        std::cout << "\n--- [ '" << keyword << "' 검색 결과 ] ---\n";
        bool found = false;
        for (const auto& book : books) {
            if (book->getTitle().find(keyword) != std::string::npos ||
                book->getAuthor().find(keyword) != std::string::npos) {
                book->printInfo();
                found = true;
            }
        }
        if (!found) {
            std::cout << "검색 결과가 없습니다.\n";
        }
    }

    // 대출 / 반납
    void borrowBook(int bookId) {
        auto it = std::find_if(books.begin(), books.end(), [bookId](const std::shared_ptr<Book>& b) {
            return b->getId() == bookId;
            });

        if (it == books.end()) {
            std::cout << ">> 오류: 해당 ID의 도서를 찾을 수 없습니다.\n";
            return;
        }

        if ((*it)->getIsBorrowed()) {
            std::cout << ">> 오류: 이미 대출 중인 도서입니다.\n";
        }
        else {
            (*it)->setBorrowed(true);
            std::cout << ">> '" << (*it)->getTitle() << "' 도서 대출이 완료되었습니다.\n";
        }
    }

    void returnBook(int bookId) {
        auto it = std::find_if(books.begin(), books.end(), [bookId](const std::shared_ptr<Book>& b) {
            return b->getId() == bookId;
            });

        if (it == books.end()) {
            std::cout << ">> 오류: 해당 ID의 도서를 찾을 수 없습니다.\n";
            return;
        }

        if (!(*it)->getIsBorrowed()) {
            std::cout << ">> 오류: 대출 중이지 않은 도서입니다.\n";
        }
        else {
            (*it)->setBorrowed(false);
            std::cout << ">> '" << (*it)->getTitle() << "' 도서 반납이 완료되었습니다.\n";
        }
    }
};

// ==========================================
// 메인 루프 (CLI 콘솔 인터페이스)
// ==========================================
int main() {
    LibraryManager library;

    int choice = 0;
    while (true) {
        std::cout << "\n===============================\n";
        std::cout << "        도서 관리 시스템  \n";
        std::cout << " ===============================\n";
        std::cout << "1. 도서 등록\n";
        std::cout << "2. 도서 삭제\n";
        std::cout << "3. 회원 등록\n";
        std::cout << "4. 회원 삭제\n";
        std::cout << "5. 전체 도서 조회\n";
        std::cout << "6. 전체 회원 조회\n";
        std::cout << "7. 도서 검색\n";
        std::cout << "8. 도서 대출\n";
        std::cout << "9. 도서 반납\n";
        std::cout << "10. 수동 데이터 저장\n";
        std::cout << "0. 종료 (자동 저장)\n";
        std::cout << "선택: ";
        std::cin >> choice;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(1000, '\n');
            std::cout << "잘못된 입력입니다. 숫자를 입력해주세요.\n";
            continue;
        }

        if (choice == 0) {
            std::cout << "프로그램을 종료합니다.\n";
            break;
        }

        std::string inputStr1, inputStr2;
        int idInput;

        switch (choice) {
        case 1:
            std::cout << "도서 제목: ";
            std::cin.ignore();
            std::getline(std::cin, inputStr1);
            std::cout << "저자 이름: ";
            std::getline(std::cin, inputStr2);
            library.addBook(inputStr1, inputStr2);
            break;

        case 2:
            std::cout << "삭제할 도서 ID: ";
            std::cin >> idInput;
            library.removeBook(idInput);
            break;

        case 3:
            std::cout << "회원 이름: ";
            std::cin.ignore();
            std::getline(std::cin, inputStr1);
            library.addUser(inputStr1);
            break;

        case 4:
            std::cout << "삭제할 회원 ID: ";
            std::cin >> idInput;
            library.removeUser(idInput);
            break;

        case 5:
            library.showAllBooks();
            break;

        case 6:
            library.showAllUsers();
            break;

        case 7:
            std::cout << "검색 키워드(제목/저자): ";
            std::cin.ignore();
            std::getline(std::cin, inputStr1);
            library.searchBook(inputStr1);
            break;

        case 8:
            std::cout << "대출할 도서 ID: ";
            std::cin >> idInput;
            library.borrowBook(idInput);
            break;

        case 9:
            std::cout << "반납할 도서 ID: ";
            std::cin >> idInput;
            library.returnBook(idInput);
            break;

        case 10:
            library.saveData();
            break;

        default:
            std::cout << "올바른 번호를 선택해주세요.\n";
            break;
        }
    }

    return 0;
}