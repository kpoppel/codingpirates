-- Lister er lidt ligesom variable, bare en struktur med flere variable i en.
-- En liste kan registreres som følgende (husk at vi skriver globale variable med stort forbogstav):
A = {}
-- 'A' er nu en tom liste, en list kan få insat værdier på flere forskellige måder:
table.insert(A, "apple") -- Her indsættes værdien på sidste plads
table.insert(A, 1, "banana") -- Her indsættes værdien på plads 1
A[3] = "orange"
-- Der kan også laves variable med navne i listen, så behøver vi ikke huske at 'apple' er på plads 2 og 'banana' på plads 1
-- Det gøres sådan:
A.berry = "cherry"
-- Vi kan nu prøve at printe A
print(A)
-- Hov, det gav da et mærkeligt output, nemlig table: 0000024AC545F4E0
-- Hvis vi vil have en specifik værdi fra 'A' så kan vi gøre det sådan:
print(A[1]) -- banana
print(A[2]) -- apple
print(A[3]) -- orange
print(A[4]) -- nil
-- Men vi har da en fjerde plads, eller hvad?
-- 'A.berry' står ikke som en plads i 'A' men nærmere som en undervariabel, den skal derfor kaldes ligesom en normal variabel:
print(A.berry) -- cherry
-- Hvis vi vil have længden af en list, kan det gøres sådan:
print(#A) -- 3 (bemærk igen at 'A.berry' ikke bliver talt med)
-- Vi må ikke indsætte værdier på andre pladser, som f.eks:
-- table.insert(A, 500, "secret") -- Kaster en fejl når lua forsøger at køre den
-- print(A[500]) -- nil
-- Hvis vi vil printe hele indholdet af 'A' kan det gøres med funktionen 'ipairs':
for index, value in ipairs(A) do
    print(index, value)
end
-- Man kan også bruge 'table.concat()':
print(table.concat(A, ", ")) -- banana, apple, orange
-- 'table.concat()' virker ikke hvis listen indeholder booleans (altså true og false), i så fald skal 'ipairs' bruges
-- For at fjerne elementer bruges 'table.remove()':
table.remove(A, 1)
print(A[1], #A) -- apple   2