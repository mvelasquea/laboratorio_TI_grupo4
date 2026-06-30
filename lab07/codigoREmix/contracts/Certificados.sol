// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Certificados { // <-- La llave se abre aquí y NO se cierra de inmediato

    struct Certificado {
        string codigo;
        string nombre;
        string metadata;
        bool valido;
    }

    uint256 private _certificadoCount;
    Certificado[] public certificados;

    event CertificadoRegistrado(string codigo, string nombre);
    event CertificadoVerificado(string codigo, bool valido);
    event ErrorRegistration(string message);

    function registrar(string memory codigo, string memory nombre, string memory metadata) public {
        for (uint i = 0; i < certificados.length; i++) {
            if (certificados[i].codigo == codigo) {
                emit ErrorRegistration("El certificado ya existe");
                return;
            }
        }
        certificados.push(Certificado({
            codigo: codigo,
            nombre: nombre,
            metadata: metadata,
            valido: true
        }));
        _certificadoCount += 1;
        emit CertificadoRegistrado(codigo, nombre);
    }

    function verificar(string memory codigo) public view returns (bool) {
        for (uint i = 0; i < certificados.length; i++) {
            if (certificados[i].codigo == codigo) {
                return certificados[i].valido;
            }
        }
        return false;
    }

    function setValidity(string memory codigo, bool valido) public {
        for (uint i = 0; i < certificados.length; i++) {
            if (certificados[i].codigo == codigo) {
                certificados[i].valido = valido;
                emit CertificadoVerificado(codigo, valido);
                return;
            }
        }
        emit ErrorRegistration("Certificado no encontrado");
    }
} // <-- La llave del contrato ahora se cierra correctamente al final
