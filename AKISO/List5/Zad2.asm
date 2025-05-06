section .data
    matrix db 34, 65, 81       ; Pierwszy wiersz
           db 14, 23, 30       ; Drugi wiersz
           db 36, 10, 72       ; Trzeci wiersz
    newline db 0x0A, 0x00      ; Nowa linia

section .bss
    sum resd 1                 ; Suma wszystkich elementów
    diag_sum resd 1            ; Suma przekątnej
    buffer resb 12             ; Bufor do konwersji liczby na ASCII

section .text
    global _start

_start:
    ; Sumowanie wszystkich liczb
    lea esi, [matrix]
    mov ecx, 9
    xor eax, eax
    mov dword [sum], 0         ; Wyzerowanie pamięci na sum
sum_all:
    movzx eax, byte [esi]      ; Załaduj wartość z tablicy
    add [sum], eax             ; Dodaj do sumy
    inc esi                    ; Przesuń wskaźnik
    loop sum_all

    ; Sumowanie przekątnej
    lea esi, [matrix]
    mov ecx, 3
    xor eax, eax
    mov dword [diag_sum], 0    ; Wyzerowanie pamięci na diag_sum
sum_diag:
    movzx eax, byte [esi]      ; Załaduj wartość z przekątnej
    add [diag_sum], eax        ; Dodaj do sumy przekątnej
    add esi, 4                 ; Przesuń wskaźnik na następną wartość
    loop sum_diag

    ; Konwersja sum do ASCII i wypisanie
    mov eax, [sum]
    lea edi, [buffer]          ; Wskaźnik na bufor
    call int_to_ascii          ; Konwertuj liczbę na ASCII
    mov eax, 4                 ; Syscall write
    mov ebx, 1                 ; Deskryptor stdout
    lea ecx, [buffer]          ; Dane do wypisania
    mov edx, 12                ; Długość danych
    int 0x80                   ; Wywołanie systemowe

    ; Syscall write
    mov eax, 4
    mov ebx, 1
    lea ecx, [newline]
    mov edx, 1
    int 0x80

    ; Konwersja diag_sum do ASCII
    mov eax, [diag_sum]
    lea edi, [buffer]
    call int_to_ascii
    ; Syscall write
    mov eax, 4
    mov ebx, 1
    lea ecx, [buffer]
    mov edx, 12
    int 0x80

    ; Syscall write
    mov eax, 4
    mov ebx, 1
    lea ecx, [newline]
    mov edx, 1
    int 0x80

    ; Syscall exit
    mov eax, 1                 
    xor ebx, ebx               
    int 0x80

; Funkcja konwertująca liczbę w eax na ASCII
; Wynik jest zapisany w buforze wskazywanym przez edi
int_to_ascii:
    add edi, 11                
    mov byte [edi], 0          
convert_to_ascii:
    dec edi                    ; Przesuń wskaźnik w lewo
    xor edx, edx               ; Wyzeruj edx (reszta z dzielenia)
    mov ebx, 10                ; Podzielnik
    div ebx                    ; eax = eax / 10, reszta w edx
    add dl, '0'                ; Konwertuj cyfrę na ASCII
    mov [edi], dl              ; Zapisz cyfrę do bufora
    test eax, eax              ; Sprawdź, czy eax = 0
    jnz convert_to_ascii       ; Jeśli nie, kontynuuj
    ret
