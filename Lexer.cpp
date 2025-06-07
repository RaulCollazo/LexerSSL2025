#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <map>
#include <fstream>
#include <sstream>

// --------------------------
// Definición de Tipos de Token
// --------------------------
enum class TokenType {
    URL, DATE, INTEGER, FLOAT, BOOLEAN, NULLVAL, VERSIONE, EMAIL,
    ILLAVE, DLLAVE, ICORCHETE, DCORCHETE, COMA, DOSPUNTOS,
    NOMBREPROPIO, STRING, INVALID, // básicos
    // Palabras reservadas (agrega aquí tus enums)
    ESTADOO, TO_DO, INPROGRESS, CANCELED, DONE, ON_HOLD,
    PRODUCT_ANALYST, PROJECT_MANAGER, DEVELOPER, MARKETING,
    UXDESIGNER, MARKETING_DEVOPS, DB_ADMIN, VERSION,
    FIRMA_DIGITAL, EQUIPOS, NOMBRE_EQUIPO, IDENTIDAD_EQUIPO,
    DIRECCION, LINK, CARRERA, ASIGNATURA, UNIVERSIDAD_REGIONAL,
    ALIANZA_EQUIPO, INTEGRANTES, PROYECTOS, CALLE, CIUDAD, PAIS,
    INTEGRANTE, NOMBRE, EDAD, CARGO, FOTO, CORREO_EMAIL, SALARIO,
    ACTIVO, HABILIDADES, PROYECTO, RESUMEN, TAREAS, FECHA_INICIO,
    FECHA_FIN, VIDEO, CONCLUSION, TAREA
};

std::map<std::string, TokenType> reserved = {
    {"\"estado\"", TokenType::ESTADOO},
    {"\"To do\"", TokenType::TO_DO},
    {"\"In progress\"", TokenType::INPROGRESS},
    {"\"Canceled\"", TokenType::CANCELED},
    {"\"Done\"", TokenType::DONE},
    {"\"On hold\"", TokenType::ON_HOLD},
    {"\"Product Analyst\"", TokenType::PRODUCT_ANALYST},
    {"\"Project Manager\"", TokenType::PROJECT_MANAGER},
    {"\"Developer\"", TokenType::DEVELOPER},
    {"\"Marketing\"", TokenType::MARKETING},
    {"\"UX designer\"", TokenType::UXDESIGNER},
    {"\"Marketing Devops\"", TokenType::MARKETING_DEVOPS},
    {"\"DB admin\"", TokenType::DB_ADMIN},
    {"\"version\"", TokenType::VERSION},
    {"\"firma_digital\"", TokenType::FIRMA_DIGITAL},
    {"\"equipos\"", TokenType::EQUIPOS},
    {"\"nombre_equipo\"", TokenType::NOMBRE_EQUIPO},
    {"\"identidad_equipo\"", TokenType::IDENTIDAD_EQUIPO},
    {"\"direccion\"", TokenType::DIRECCION},
    {"\"link\"", TokenType::LINK},
    {"\"carrera\"", TokenType::CARRERA},
    {"\"asignatura\"", TokenType::ASIGNATURA},
    {"\"universidad_regional\"", TokenType::UNIVERSIDAD_REGIONAL},
    {"\"alianza_equipo\"", TokenType::ALIANZA_EQUIPO},
    {"\"integrantes\"", TokenType::INTEGRANTES},
    {"\"proyectos\"", TokenType::PROYECTOS},
    {"\"calle\"", TokenType::CALLE},
    {"\"ciudad\"", TokenType::CIUDAD},
    {"\"pais\"", TokenType::PAIS},
    {"\"integrante\"", TokenType::INTEGRANTE},
    {"\"nombre\"", TokenType::NOMBRE},
    {"\"edad\"", TokenType::EDAD},
    {"\"cargo\"", TokenType::CARGO},
    {"\"foto\"", TokenType::FOTO},
    {"\"email\"", TokenType::CORREO_EMAIL},
    {"\"salario\"", TokenType::SALARIO},
    {"\"activo\"", TokenType::ACTIVO},
    {"\"habilidades\"", TokenType::HABILIDADES},
    {"\"proyecto\"", TokenType::PROYECTO},
    {"\"resumen\"", TokenType::RESUMEN},
    {"\"tareas\"", TokenType::TAREAS},
    {"\"fecha_inicio\"", TokenType::FECHA_INICIO},
    {"\"fecha_fin\"", TokenType::FECHA_FIN},
    {"\"video\"", TokenType::VIDEO},
    {"\"conclusión\"", TokenType::CONCLUSION},
    {"\"tarea\"", TokenType::TAREA}
};

struct Token {
    TokenType type;
    std::string value;
    int lineno, col;
};

std::string tokenTypeToStr(TokenType type) {
    // Puedes mejorar este mapeo para imprimir el nombre como string
    switch(type) {
        case TokenType::URL: return "URL";
        case TokenType::DATE: return "DATE";
        case TokenType::FLOAT: return "FLOAT";
        case TokenType::INTEGER: return "INTEGER";
        case TokenType::BOOLEAN: return "BOOLEAN";
        case TokenType::NULLVAL: return "NULL";
        case TokenType::VERSIONE: return "VERSIONE";
        case TokenType::EMAIL: return "EMAIL";
        case TokenType::ILLAVE: return "ILLAVE";
        case TokenType::DLLAVE: return "DLLAVE";
        case TokenType::ICORCHETE: return "ICORCHETE";
        case TokenType::DCORCHETE: return "DCORCHETE";
        case TokenType::COMA: return "COMA";
        case TokenType::DOSPUNTOS: return "DOSPUNTOS";
        case TokenType::NOMBREPROPIO: return "NOMBREPROPIO";
        case TokenType::STRING: return "STRING";
        case TokenType::INVALID: return "INVALID";
        default: return "RESERVED/PALABRA";
    }
}

// --------------------------
// Definición de patrones regex
// --------------------------
std::vector<std::pair<TokenType, std::regex>> token_regexes = {
    {TokenType::EMAIL, std::regex("\"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z]{2,4}\"")},
    {TokenType::URL, std::regex("\"(https?|ftp)://[^\\s\"]+\"")},
    {TokenType::DATE, std::regex("\"(19[0-9]{2}|20[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\"")},
    {TokenType::NULLVAL, std::regex("null")},
    {TokenType::VERSIONE, std::regex("\"\\d+\\.\\d{1,2}\"")},
    {TokenType::FLOAT, std::regex("\\d+\\.\\d+")},
    {TokenType::INTEGER, std::regex("\\d+")},
    {TokenType::BOOLEAN, std::regex("true|false")},
    {TokenType::NOMBREPROPIO, std::regex("\"[A-Z][a-z]+ [A-Z][a-z]+\"")},
    {TokenType::ILLAVE, std::regex("\\{")},
    {TokenType::DLLAVE, std::regex("\\}")},
    {TokenType::ICORCHETE, std::regex("\\[")},
    {TokenType::DCORCHETE, std::regex("\\]")},
    {TokenType::COMA, std::regex(",")},
    {TokenType::DOSPUNTOS, std::regex(":")},
    {TokenType::STRING, std::regex("\"([^\\\\\\n]|(\\\\.))*?\"")}
    // Reservadas se reconocen después
};

Token getNextToken(const std::string &input, size_t &pos, int lineno, int &col) {
    if (pos >= input.size()) return {TokenType::INVALID, "", lineno, col};

    while (pos < input.size() && (input[pos] == ' ' || input[pos] == '\t' || input[pos] == '\n')) {
        if (input[pos] == '\n') { lineno++; col = 0; }
        else col++;
        pos++;
    }
    if (pos >= input.size()) return {TokenType::INVALID, "", lineno, col};

    // Probar palabras reservadas primero
    for (const auto& r : reserved) {
        size_t len = r.first.size();
        if (input.compare(pos, len, r.first) == 0) {
            Token t{r.second, r.first, lineno, col};
            pos += len;
            col += len;
            return t;
        }
    }

    // Probar regexs
    for (const auto& tr : token_regexes) {
        std::smatch match;
        std::string sub = input.substr(pos);
        if (std::regex_search(sub, match, tr.second) && match.position() == 0) {
            Token t{tr.first, match.str(0), lineno, col};
            pos += match.length(0);
            col += match.length(0);
            return t;
        }
    }

    // Si nada coincide: inválido
    std::string inval(1, input[pos]);
    Token t{TokenType::INVALID, inval, lineno, col};
    pos++; col++;
    return t;
}

void analizar(const std::string& data) {
    size_t pos = 0;
    int lineno = 1, col = 0;
    while (pos < data.size()) {
        Token tok = getNextToken(data, pos, lineno, col);
        if (tok.type == TokenType::INVALID && tok.value.empty()) break;
        if (tok.type == TokenType::INVALID)
            std::cout << "Error léxico: token ilegal '" << tok.value << "' en línea " << tok.lineno << ", columna " << tok.col << std::endl;
        else
            std::cout << "Se ha encontrado el token: '" << tok.value << "' del tipo: " << tokenTypeToStr(tok.type) << std::endl;
    }
}

int main() {
    std::cout << "¿Desea analizar Léxicamente un string o un archivo?\n";
    while (true) {
        std::cout << "Menú de opciones" << std::endl;
        std::cout << "1. Realizar el análisis léxico de forma manual" << std::endl;
        std::cout << "2. Analizar un archivo.json específico" << std::endl;
        std::cout << "3. Salir" << std::endl;
        int opcion;
        std::cout << "Elige una opción (1-3): ";
        std::cin >> opcion;
        std::cin.ignore();
        if (opcion == 1) {
            std::string data;
            std::cout << "Ingrese el texto a analizar: ";
            std::getline(std::cin, data);
            analizar(data);
        } else if (opcion == 2) {
            std::string ruta;
            std::cout << "Ingrese la ruta del archivo .json: ";
            std::getline(std::cin, ruta);
            std::ifstream file(ruta);
            if (!file) {
                std::cout << "No se pudo encontrar el archivo en la ruta: " << ruta << std::endl;
            } else {
                std::stringstream buffer;
                buffer << file.rdbuf();
                analizar(buffer.str());
            }
        } else if (opcion == 3) {
            std::cout << "Saliendo del programa..." << std::endl;
            break;
        } else {
            std::cout << "Opción no válida. Por favor, elige una opción del 1 al 3." << std::endl;
        }
    }
    return 0;
}
