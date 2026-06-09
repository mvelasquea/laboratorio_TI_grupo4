// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./contracts/Certificados.sol";

contract CertificadosTest {
    Certificados certificados;
    
    function setup() public {
        certificados = Certificados();
    }
    
    function testRegistroExitoso() public {
        setup();
        string memory codigo = "UNSA-2026-0041";
        string memory nombre = "Mikhail Gabino Velasquez Arcos";
        
        certificados.registrar(codigo, nombre, "");
        assert(certificados.existe(codigo) == true);
    }
    
    function testVerificacionExistente() public {
        setup();
        string memory codigo = "UNSA-2026-0041";
        string memory nombre = "Mikhail Gabino Velasquez Arcos";
        
        certificados.registrar(codigo, nombre, "");
        bool resultado = certificados.verificar(codigo);
        assert(resultado == true);
    }
    
    function testVerificacionInexistente() public {
        setup();
        string memory codigo = "FRAUDE-2026-9999";
        bool resultado = certificados.verificar(codigo);
        assert(resultado == false);
    }
    
    function testRegistroDenegadoDuplicado() public {
        setup();
        string memory codigo = "UNSA-2026-0041";
        string memory nombre = "Mikhail Gabino Velasquez Arcos";
        
        certificados.registrar(codigo, nombre, "");
        assertThrows(certificados.registrar(codigo, "NuevoNombre", ""));
    }
    
    function testRegistroDenegadoVacioNombre() public {
        setup();
        string memory codigo = "UNSA-2026-0042";
        
        assertThrows(certificados.registrar(codigo, "", ""));
    }
    
    function testRegistroDenegadoSinMetadata() public {
        setup();
        string memory codigo = "UNSA-2026-0043";
        string memory nombre = "NombreTest";
        
        assertThrows(certificados.registrar(codigo, nombre, ''));
    }
}