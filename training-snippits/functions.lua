-- En funktion er lidt ligesom en variabel, den har bare et stykke kode i stedet for en værdi
-- Eksempel:
-- Vi vil gerne kunne beregne summen plus produktet af 2 tal, det kan gøres på følgende måde:
local a = 5
local b = 6
local c = a + b + a * b
print(c)
-- Denne metode giver et svar og vi kan ændre svaret ved at ændre vores variable a og b, 
-- men hvad nu hvis vi gerne vil kunne gøre det med kun en kommando?
-- Så kan vi bruge en funktion:
local function sumOfNumbers(a, b)
    return a + b + a * b
end
-- Bemærk at "a" og "b" i funktionen ikke er de samme "a" og "b" som uden for funktionen, da de tager prioritet.
-- Når vi vil bruge funktionen kalder vi den som følgende, i det her tilfælde giver den en værdi, og vi printer den til konsollen:
print(sumOfNumbers(1,2)) -- Output: 5 //(1+2 + 1*2)
-- "a" og "b" i funktionen hedder parametre, og det er en god måde at sende værdier ind i funktionen, så den ikke ændrer nogle variable