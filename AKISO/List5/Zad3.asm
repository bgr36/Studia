section .data
    liczba dd 4294967295                ; Liczba do konwersji (32-bitowa)
    buffer db "00000000", 10, 0     ; Bufor na wynik HEX + znak nowej linii + null terminator
    hex_chars db "0123456789ABCDEF" ; Znaki szesnastkowe
    newline db 0x0A, 0x00 
    
section .text
    global _start

_start:
    ; Wczytaj liczbę
    mov eax, [liczba]               
    lea esi, [buffer+7]             

    ; Konwersja liczby na hex
.hex_convert:
    mov ecx, eax                    ; Skopiuj liczbę do ECX
    and ecx, 0xF                    ; Wyodrębnij 4 najmłodsze bity (jeden znak HEX)
    mov bl, byte [hex_chars + ecx]  ; Pobierz odpowiedni znak HEX
    mov byte [esi], bl              ; Zapisz znak do bufora
    dec esi                         ; Przesuń wskaźnik bufora w lewo
    shr eax, 4                      ; Przesuń liczbę o 4 bity w prawo
    test eax, eax                   ; Sprawdź, czy liczba została całkowicie przetworzona
    jnz .hex_convert                ; Jeśli nie, kontynuuj pętlę

    ; Ustaw wskaźnik na początek liczby w buforze
    lea edi, [buffer]               ; Ustaw wskaźnik na bufor
    mov ecx, 8                      ; Maksymalnie 8 znaków HEX
.skip_zeros:
    cmp byte [edi], '0'             ; Sprawdź, czy aktualny znak to '0'
    jne .write_result               ; Jeśli nie, zakończ usuwanie zer wiodących
    inc edi                         ; Przejdź do następnego znaku
    dec ecx                         ; Zmniejsz liczbę znaków do wypisania
    jmp .skip_zeros

.write_result:
    ; Syscall write 
    mov eax, 4                      
    mov ebx, 1                      
    mov edx, ecx                    
    mov ecx, edi                    
    int 0x80                        

    ; Syscall write 
    mov eax, 4
    mov ebx, 1
    lea ecx, [newline]
    mov edx, 1
    int 0x80

    ; Syscal exit
    mov eax, 1                      
    xor ebx, ebx                    
    int 0x80                        
