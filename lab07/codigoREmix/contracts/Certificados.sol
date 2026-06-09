// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Certificados { // <-- La llave se abre aquí y NO se cierra de inmediato

    struct Certificado {
        string codigo;
        string nombre;
        string metadata;
        bool valido;
    }

    mapping(bytes32 => bool) public _exists;
    mapping(bytes32 => Certificado) public certificados;

    event CertificadoRegistrado(string codigo, string nombre);
    event CertificadoVerificado(string codigo, bool valido);
    event ErrorRegistration(string message);

    function registrar(
        string memory codigo,
        string memory nombre,
        string memory metadata
    ) public {
        bytes32 key = keccak256(abi.encodePacked(codigo));
        if (_exists[key]) {
            emit ErrorRegistration("El certificado ya existe");
            return;
        }
        certificados[key] = Certificado({
            codigo: codigo,
            nombre: nombre,
            metadata: metadata,
            valido: true
        });
        _exists[key] = true;
        emit CertificadoRegistrado(codigo, nombre);
    }

    function verificar(string memory codigo) public view returns (bool) {
        bytes32 key = keccak256(abi.encodePacked(codigo));
        if (!_exists[key]) {
            return false;
        }
        return certificados[key].valido;
    }

    function setValidity(string memory codigo, bool valido) public {
        bytes32 key = keccak256(abi.encodePacked(codigo));
        if (!_exists[key]) {
            emit ErrorRegistration("Certificado no encontrado");
            return;
        }
        certificados[key].valido = valido;
        emit CertificadoVerificado(codigo, valido);
    }
} // <-- La llave del contrato ahora se cierra correctamente al final
