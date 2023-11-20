#include <Arduino.h>

// Colocar o baudrate desejado para leitura
int SerialConvertion()
{
    String palavra = " ";
    char c;
    if (Serial.available() > 0)
    {
        c = (Serial.read());
        if (c == (','))
        {
            while (c != '/')
            {
                int i = 0;
                if (Serial.available() > 0)
                {   
                    c = char(Serial.read());
                    i++;
                    if (i < 2)
                    {
                        
                        Serial.println(c);
                        palavra = palavra + c;
                    }
                }
            }
            Serial.println(palavra);
            int eixoX = palavra.toInt();
            Serial.println(eixoX);
            return eixoX;
        }
    }
    else
    {
        return 0;
    }
}
