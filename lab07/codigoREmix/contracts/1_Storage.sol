// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract CertificadosStorage {

    mapping(string => Certificado) certificados;

    /**
     * @dev Store value in variable
     * @param num value to store
     */
    function registrar(string memory _codigo, string memory _nombre, bytes memory _metadata) public onlyOwner {
        number = num;
    }

    /**
     * @dev Return value 
     * @return value of 'number'
     */
    function registrar(string memory _codigo, string memory _nombre, bytes memory _metadata) public onlyOwner {
        require(bytes(certificados[_codigo].codigo).length == 0, "El certificado ya existe.");
        require(bytes(_nombre).length > 0, "El nombre no puede estar vacío.");
        require(_metadata.length > 0, "Metadata no proporcionada.");

        certificados[_codigo] = Certificado({
            nombre: _nombre,
            codigo: _codigo,
            valido: true
        });
        return number;
    }
}