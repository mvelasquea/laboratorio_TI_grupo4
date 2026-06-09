const { expect } = require('chai');
const { ethers } = require('ethers');
const { solidity } = require('ethereum-waffle');

describe('Certificados Contract', function () {
    let certificados;
    let owner;
    let signer;
    
    before(async () => {
        [signer] = await ethers.getSigners();
        certificados = await ethers.getContractFactory('Certificados').deploy();
        await certificados.deployed();
        owner = signer.address;
    });
    
    describe('Registro de Certificado', function () {
        it('Registrar un certificado exitosamente', async () => {
            const codigo = 'UNSA-2026-0041';
            const nombre = 'Mikhail Gabino Velasquez Arcos';
            const metadata = '';

            await certificados.connect(owner).registrar(codigo, nombre, metadata);

            // Validar que el certificado exista y esté registrado
            const certificado = await certificados.certificados(codigo);
            expect(certificado.nombre).to.equal(nombre);
            expect(certificado.valido).to.equal(true);
        });
    });
    
    describe('Verificación de Certificado', function () {
        it('Debería devolver true para un certificado registrado', async () => {
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
            const nombre = 'Prueba duplicada';

            await certificados.connect(owner).registrar(codigo, nombre, '');
            await expect(certificados.connect(owner).registrar(codigo, 'Nuevo nombre', '')).to.be.revertedWith('El certificado ya existe');
        });
    });
});