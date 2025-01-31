// Created by Shrekulka on 18.10.2023.


// Наш заголовочный файл, который подключается перед любыми
// стандартными системными заголовочными файлами


// Директивы препроцессора для защиты от множественного включения файла.
#ifndef DIRECTORY_FILE_LISTING_APUE_H
#define DIRECTORY_FILE_LISTING_APUE_H

// Определение стандартов POSIX и X/Open в зависимости от платформы.
#define _POSIX_C_SOURCE 200809L
#if defined(SOLARIS) /* Solaris 10 */
#define _XOPEN_SOURCE 600
#else
#define _XOPEN_SOURCE 700
#endif


#include <sys/types.h>
#include <sys/stat.h>
#include <sys/termios.h> // структура winsize

// Обычно такие условия используются для настройки компиляции программы в зависимости от конкретной платформы.
// `TIOCGWINSZ` является макросом, используемым в программировании в среде UNIX-подобных операционных систем. Он
// используется для получения информации о размерах окна терминала (ширине и высоте) в терминале. Этот макрос обычно
// используется с системными вызовами, такими как `ioctl` для получения информации о размере терминала, что может быть
// полезно для настройки вывода и взаимодействия с пользователем в текстовом режиме.
// Когда `TIOCGWINSZ` не определен (как в вашем коде), это означает, что он не доступен, и программе приходится
// использовать альтернативные способы для определения размеров окна терминала.
//`TIOCGWINSZ` может быть определен в заголовочных файлах, связанных с работой с терминалами и окнами в разных системах.
#if defined(MACOS) || !defined(TIOCGWINSZ)

#include <sys/ioctl.h>

#endif

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include <signal.h> // константа SIG_ERR

// Определение максимальной длины строки.
#define MAXLINE 4096

// Права доступа по умолчанию к создаваемым файлам.
#define FILE_MODE (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

// Права доступа по умолчанию к создаваемым каталогам.
#define DIR_MODE (FILE_MODE | S_IXUSR | S_IXGRP | S_IXOTH)

// Определение пользовательского типа Sigfunc для обработчиков сигналов.
typedef void Sigfunc(int); /* обработчики сигналов */

// Определение макросов для нахождения минимума и максимума.
#define min(a, b) ((a) < (b) ? (a) : (b))
#define max(a, b) ((a) > (b) ? (a) : (b))



// Прототипы наших собственных функций.


// Выделяет память для строки пути и возвращает указатель на нее, также сохраняя размер в аргументе size.
char* path_alloc(size_t*);

// Возвращает максимальное количество открытых файловых дескрипторов.
long open_max(void);

// Устанавливает флаг FD_CLOEXEC для указанного файлового дескриптора.
int set_cloexec(int);

// Очищает биты флагов указанного файлового дескриптора.
void clr_fl(int, int);

// Устанавливает биты флагов указанного файлового дескриптора.
void set_fl(int, int);

// Выводит информацию о статусе завершения процесса.
void pr_exit(int);

// Выводит текущую маску сигналов процесса.
void pr_mask(const char*);

// Устанавливает обработчик сигнала и возвращает предыдущий обработчик.
Sigfunc* signal_intr(int, Sigfunc*);

// Демонизирует процесс, отсоединяя его от терминала и создавая новую сессию.
void daemonize(const char*);

// Переводит процесс в спящий режим на заданное количество микросекунд.
void sleep_us(unsigned int);

// Читает из файла до заданного числа байтов и возвращает количество прочитанных байтов.
ssize_t readn(int, void*, size_t);

// Записывает в файл заданное количество байтов и возвращает количество записанных байтов.
ssize_t writen(int, const void*, size_t);

// Создает канал pipe и возвращает два файловых дескриптора.
int fd_pipe(int*);

// Получает файловый дескриптор через сокет и передает его указанной функции.
int recv_fd(int, ssize_t (* func)(int, const void*, size_t));

// Отправляет файловый дескриптор через сокет.
int send_fd(int, int);

// Отправляет сообщение об ошибке через сокет.
int send_err(int, int, const char*);

// Создает серверный сокет для прослушивания и возвращает его файловый дескриптор.
int serv_listen(const char*);

// Принимает клиентское соединение на указанном сокете и возвращает клиентский файловый дескриптор.
int serv_accept(int, uid_t*);

// Подключается к серверу и возвращает файловый дескриптор клиента.
int cli_conn(const char*);

// Разбивает аргументы командной строки и передает их указанной функции.
int buf_args(char*, int (* func)(int, char**));

// Устанавливает режим "cbreak" для терминала, отключая буферизацию и ввод в режиме каракулей.
int tty_cbreak(int);

// Устанавливает режим "raw" для терминала, отключая обработку специальных символов.
int tty_raw(int);

// Сбрасывает режим терминала к значениям по умолчанию.
int tty_reset(int);

// Устанавливает функцию, которая будет вызвана при завершении работы программы.
void tty_atexit(void);

// Получает структуру termios для терминала.
struct termios* tty_termios(void);

// Создает мастер-псевдотерминал (pty).
int ptym_open(char*, int);

// Открывает слейв-псевдотерминал (pty).
int ptys_open(char*);

#ifdef TIOCGWINSZ
// Создает дочерний процесс для работы с псевдотерминалом (pty).
pid_t pty_fork(int*, char*, int, const struct termios*, const struct winsize*);
#endif



// Прототипы и макросы для функций и блокировок файлов.


// Выполняет блокировку файла с заданными параметрами.
int lock_reg(int, int, int, off_t, int, off_t);

// Макрос для установки блокировки чтения.
// Принимает аргументы:
// - fd: файловый дескриптор, на который будет установлена блокировка;
// - offset: смещение в файле, с которого начнется блокировка;
// - whence: способ интерпретации смещения (SEEK_SET, SEEK_CUR или SEEK_END);
// - len: размер блокировки.
#define read_lock(fd, offset, whence, len) ...

// Макрос для установки блокировки чтения с ожиданием.
// Принимает аргументы аналогично макросу read_lock.
#define readw_lock(fd, offset, whence, len) ...

// Макрос для установки блокировки записи.
// Принимает аргументы аналогично макросу read_lock.
#define write_lock(fd, offset, whence, len) ...

// Макрос для установки блокировки записи с ожиданием.
// Принимает аргументы аналогично макросу read_lock.
#define writew_lock(fd, offset, whence, len) ...

// Макрос для снятия блокировки.
// Принимает аргументы аналогично макросу read_lock.
#define un_lock(fd, offset, whence, len) ...

// Проверяет, можно ли установить блокировку на файл.
// Принимает аргументы:
// - fd: файловый дескриптор, на который будет установлена блокировка;
// - type: тип блокировки (F_RDLCK для чтения или F_WRLCK для записи);
// - offset: смещение в файле, с которого начнется блокировка;
// - whence: способ интерпретации смещения (SEEK_SET, SEEK_CUR или SEEK_END);
// - len: размер блокировки.
pid_t lock_test(int, int, off_t, int, off_t);

// Макрос для проверки возможности установки блокировки чтения.
// Принимает аргументы аналогично макросу lock_test.
#define is_read_lockable(fd, offset, whence, len) ...

// Макрос для проверки возможности установки блокировки записи.
// Принимает аргументы аналогично макросу lock_test.
#define is_write_lockable(fd, offset, whence, len) ...



// Прототипы функций для обработки ошибок и журналирования.


// Выводит сообщение об ошибке и продолжает выполнение программы.
void err_msg(const char*, ...);

// Выводит сообщение об ошибке, завершает программу и выводит сообщение о системной ошибке.
void err_dump(const char*, ...) __attribute__((noreturn));

// Выводит сообщение об ошибке и завершает программу.
void err_quit(const char*, ...) __attribute__((noreturn));

// Выводит сообщение об ошибке и продолжает выполнение программы.
void err_cont(int, const char*, ...);

// Выводит сообщение об ошибке, завершает программу с заданным кодом ошибки.
void err_exit(int, const char*, ...) __attribute__((noreturn));

// Выводит сообщение об ошибке и продолжает выполнение программы.
void err_ret(const char*, ...);

// Выводит сообщение об ошибке, завершает программу и выводит сообщение о системной ошибке.
void err_sys(const char*, ...) __attribute__((noreturn));

// Выводит сообщение в журнал.
void log_msg(const char*, ...);

// Открывает файл для журналирования.
void log_open(const char*, int, int);

// Выводит сообщение в журнал и завершает программу.
void log_quit(const char*, ...) __attribute__((noreturn));

// Выводит сообщение в журнал и продолжает выполнение программы.
void log_ret(const char*, ...);

// Выводит сообщение в журнал, завершает программу и выводит сообщение о системной ошибке.
void log_sys(const char*, ...) __attribute__((noreturn));

// Выводит сообщение в журнал, завершает программу с заданным кодом ошибки.
void log_exit(int, const char*, ...) __attribute__((noreturn));



// Дополнительные функции для синхронизации процессов.


// Инициализирует средства синхронизации между родительским и дочерним процессами.
void TELL_WAIT(void);

// Сообщает родительскому процессу.
void TELL_PARENT(pid_t);

// Сообщает дочернему процессу.
void TELL_CHILD(pid_t);

// Ожидает сообщения от родительского процесса.
void WAIT_PARENT(void);

// Ожидает сообщения от дочернего процесса.
void WAIT_CHILD(void);


#endif //DIRECTORY_FILE_LISTING_APUE_H
// Конец директивы защиты от множественного включения файла.
