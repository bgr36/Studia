section .data
    prompt db "Podaj liczbe: ", 0x0A, 0x00    ; Komunikat do wyświetlenia
    result_msg db "Suma cyfr: ", 0x00         ; Komunikat wyniku
    newline db 0x0A, 0x00                     ; Znak nowej linii
    buffer_size equ 32                        ; Rozmiar bufora do wczytywania danych

section .bss
    buffer resb buffer_size                   ; Bufor na wczytane dane
    sum resd 1                                ; Miejsce na sumę cyfr (32-bitowe)

section .text
    global _start

_start:
    ; Syscall write
    mov eax, 4            
    mov ebx, 1             
    mov ecx, prompt        
    mov edx, 15             
    int 0x80

    ; Syscall read
    mov eax, 3              
    mov ebx, 0              
    mov ecx, buffer         
    mov edx, buffer_size    
    int 0x80

    ; Zeruj sumę cyfr
    xor eax, eax            
    mov [sum], eax          

    ; Oblicz sumę cyfr
    mov esi, buffer         ; Adres pierwszego znaku w buforze
compute_sum:
    lodsb                   ; Załaduj bajt z [esi] do al, zwiększ esi
    cmp al, 0x0A            ; Sprawdź, czy znak to nowa linia (koniec liczby)
    je print_result         ; Jeśli tak, przejdź do wyświetlenia wyniku
    cmp al, 0x30            ; Sprawdź, czy znak jest cyfrą ('0')
    jb compute_sum          ; Jeśli nie, pomiń ten znak
    cmp al, 0x39            ; Sprawdź, czy znak jest cyfrą ('9')
    ja compute_sum          ; Jeśli nie, pomiń ten znak
    sub al, '0'             ; Konwertuj ASCII na wartość cyfry
    mov ebx, [sum]          ; Pobierz obecną sumę cyfr
    add ebx, eax            ; Dodaj cyfrę do sumy
    mov [sum], ebx          ; Zapisz nową sumę
    jmp compute_sum         ; Wróć do przetwarzania kolejnego znaku

print_result:
    ; Syscall write
    mov eax, 4              
    mov ebx, 1              
    mov ecx, result_msg     
    mov edx, 12             
    int 0x80

    ; Konwertuj sumę cyfr na ciąg ASCII
    mov eax, [sum]          ; Wczytaj sumę z pamięci
    mov edi, buffer         ; Ustaw wskaźnik na koniec bufora
    add edi, buffer_size    ; Przesuń wskaźnik poza bufor
    call int_to_ascii       ; Wywołaj procedurę konwersji

    ; Syscall write
    mov ecx, edi            
    sub edi, eax            
    mov eax, 4              
    mov ebx, 1              
    mov ecx, edi            
    mov edx, eax            
    int 0x80

    ; Syscall write
    mov eax, 4              
    mov ebx, 1              
    mov ecx, newline        
    mov edx, 1              
    int 0x80

    ; Syscall exit
    mov eax, 1              
    xor ebx, ebx            
    int 0x80

; Funkcja konwertująca liczbę w eax na ASCII
; Wynik jest zapisany w buforze wskazywanym przez edi
int_to_ascii:
    xor ecx, ecx            
    mov ebx, 10             
convert_to_ascii:
    xor edx, edx            ; Zerowanie EDX przed dzieleniem
    div ebx                 ; Dzielenie EAX przez EBX, reszta w EDX
    add dl, '0'             ; Zamiana reszty (cyfry) na ASCII
    dec edi                 ; Przesuń wskaźnik na buforze
    mov [edi], dl           ; Zapisz cyfrę w buforze
    inc ecx                 ; Zwiększ licznik cyfr
    test eax, eax           ; Sprawdź, czy dzielenie zakończone
    jnz convert_to_ascii:   ; Jeśli nie, kontynuuj
    mov eax, ecx            ; Licznik cyfr do eax (dla długości wyniku)
    ret
