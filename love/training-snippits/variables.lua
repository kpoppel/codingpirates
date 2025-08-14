-- Alle variable og funktioner anses som globale, medmindre de har "local" skrevet foran sig
-- Variable kan tildeles en værdi
A = 10
B = 5

-- Værdien kan også tildeles fra andre variable
C = A + B

print(A,B,C)

function Var()
    -- Lokale variable erklæres med brug af prefikset "local"
    local d = 20

    -- Lokale variable tager prioritet over globale variable
    local A = 100

    -- Globale variable kan ændres i lokale sammenhæng, hvilket giver en ændring alle steder
    B = 1

    -- Både lokale og globale variable kan tilgås i lokal sammenhæng
    print(C,d,A)

    -- Funktioner kan også være lokale, de følger samme regler som lokale variable
    local function varloc()
        -- Igen kan alle variable tilgås
        print("Hello World", A, B, C, d)
    end

    varloc()
end

Var()
-- Uden for "Var" kan den lokale variabel "d" ikke tilgås, den får derfor værdien "nil"
print(A,B,C,d)

-- Uden for "Var" er funktionen "varloc" ikke registreret og kan derfor ikke kaldes
varloc()
