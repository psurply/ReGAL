#include <stdlib.h>
#include <avr/io.h>


static inline void uart_init(void)
{
    UBRR0H = 0;
    UBRR0L = 16;
    UCSR0A = (1 << U2X0);
    UCSR0B = (1 << RXCIE0) | (1 << TXEN0) | (1 << RXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}


static inline void uart_send(uint8_t c)
{
    while (!((UCSR0A >> UDRE0) & 1))
        continue;
    UDR0 = c;
}


static inline uint8_t uart_rx_avl(void)
{
    return (UCSR0A >> RXC0) & 1;
}


static inline uint8_t uart_recv(void)
{
    while (!((UCSR0A >> RXC0) & 1))
        continue;
    return UDR0;
}


static inline void gpio_init(uint8_t output_mask)
{
    DDRC = 0xFF;
    DDRL = 0xFF;
    DDRA = output_mask;
}


static inline uint8_t get_output_value(uint8_t output_mask, uint8_t value)
{
    uint8_t out = 0;
    uint8_t offset = 0;

    for (uint8_t i = 0; i < 8; ++i) {
        if ((output_mask >> i) & 1) {
            out |= ((value >> offset) & 1) << i;
            offset++;
        } else {
            out |= 1 << i;
        }
    }

    return out;
}


static inline void dump_tables(uint32_t start, uint8_t output_mask)
{
    const uint8_t fixed_input_size = 14;

    for (uint32_t i = 0; i < 0xFFF; ++i) {
        uart_send(0);
    }

    for (uint32_t i = start; i < 0xFFFFFF; ++i) {
        while (uart_rx_avl()) {
            if (uart_recv() == 's')
                return;
        }

        PORTC = i & 0xFF;
        PORTL = (i >> 8) & 0xFF;
        PORTA = get_output_value(output_mask, (i >> fixed_input_size) & 0xFF);

        uart_send(0x02);
        uart_send(PORTC);
        uart_send(PORTL);
        uart_send(PINA);
   }
}


int main(void)
{
    uint32_t start = 0;
    uint8_t output_mask = 0;
    uint8_t cmd = 0;

    uart_init();
    gpio_init(0);

    for (;;) {
        cmd = uart_recv();

        if (cmd == 'd') {
            output_mask = uart_recv();
            gpio_init(output_mask);
        }
 
        if (cmd == 'r') {
            start = uart_recv();
            start = (start << 8) | uart_recv();
            start = (start << 8) | uart_recv();
            start = (start << 8) | uart_recv();
        }

        if (cmd == 'p') {
            dump_tables(start, output_mask);
        }
    }

    return 0;
}
