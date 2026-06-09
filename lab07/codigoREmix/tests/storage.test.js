const { expect } = require('chai');
const { ethers } = require('ethers');
const { solidity } = require('ethereum-waffle');

describe('Certificados Contract Tests', function () {
    let certificados;
    let owner;
    let signers;
    
    before(async () => {
        [signers] = await ethers.getSigners();
        certificados = await ethers.getContractFactory('Certificados').deploy();
        await certificados.deployed();
        owner = signers[0].address;
    });
    
    describe('Registro de Certificado', function () {
        it('Debería registrar correctamente un certificado', async () => {
            const codigo = 'UNSA-2026-0041';
            const nombre = 'Mikhail Gabino Velasquez Arcos';
            
            await certificados.connect(owner).registrar(codigo, nombre, '');
            
            const certificado = await certificados.certificados(codigo);
            expect(certificado.nombre).to.equal(nombre);
            expect(certificado.valido).to.equal(true);
        });
    });
    
    describe('Verificación de Certificado', function () {
        it('Debería devolver true para un certificado existente', async () => {
            const codigo = 'UNSA-2026-0041';
            const nombre = 'Mikhail Gabino Velasquez Arcos';
            
            await certificados.connect(owner).registrar(codigo, nombre, '');
            
            const resultado = await certificados.verificar(codigo);
            expect(resultado).to.equal(true);
        });
        
        it('Debería devolver false para un certificado inexistente', async () => {
            const codigo = 'FRAUDE-2026-9999';
            
            const resultado = await certificados.verificar(codigo);
            expect(resultado).to.equal(false);
        });
    });
    
    describe('Restricciones de Registro', function () {
        it('Debería rechazar registros con código duplicado', async () => {
            const codigo = 'UNSA-2026-0041';
            const nombre = 'NuevoNombre';
            
            await certificados.connect(owner).registrar(codigo, nombre, '');
            
            await expect(certificados.connect(owner).registrar(codigo, 'NuevoNombre', ''))
                .to.be.revertedWith('El certificado ya existe.');
        });
        
        it('Debería rechazar registros con nombre vacío', async () => {
            const codigo = 'UNSA-2026-0042';
            
            await expect(certificados.connect(owner).registrar(codigo, '', ''))
                .to.be.revertedWith('El nombre no puede estar vacío.');
        });
        
        it('Debería rechazar registros sin metadata', async () => {
            const codigo = 'UNSA-2026-0043';
            const nombre = 'NombreTest';
            
            await expect(certificados.connect(owner).registrar(codigo, nombre, ''))
                .to.be.revertedWith('Metadata no proporcionada.');
        });
    });
});