#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para consolidar a TERCEIRA ABA (Municípios das Capitais)
das Tabelas 12.1 a 12.8 em um formato tabular estruturado.
"""

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os


def consolidar_tabelas_municipios(diretorio_origem=None):
    """
    Consolida as Tabelas 12.1 a 12.8 (terceira aba) em um arquivo Excel estruturado
    com Municípios das Capitais.
    
    Args:
        diretorio_origem (str): Diretório contendo os arquivos. Se None, usa o diretório atual.
    """
    
    if diretorio_origem is None:
        diretorio_origem = "/Users/amartins/gitlab"
    
    # Arquivos a processar com suas informações
    arquivos = [
        ("Tabelas 12.1.xlsx", "12.1.3", "NÃO_TEM_AMIGO_PROXIMO"),
        ("Tabelas 12.2.xlsx", "12.2.3", "MUITO_PREOCUPADO"),
        ("Tabelas 12.3.xlsx", "12.3.3", "TRISTE"),
        ("Tabelas 12.4.xlsx", "12.4.3", "SOZINHO"),
        ("Tabelas 12.5.xlsx", "12.5.3", "PROBLEMA_CONCENTRACAO"),
        ("Tabelas 12.6.xlsx", "12.6.3", "PROBLEMA_INSONIA"),
        ("Tabelas 12.7.xlsx", "12.7.3", "SENTIMENTO_INUTILIDADE"),
        ("Tabelas 12.8.xlsx", "12.8.3", "PENSAMENTO_MORTE"),
    ]
    
    # Criar workbook consolidado
    wb_consolidado = Workbook()
    ws_consolidado = wb_consolidado.active
    
    # Definir cabeçalhos para terceira aba
    cabecalhos = [
        "TABELA_ORIGEM", "NOME_METRICA", "Municipio", "rc",
        "Limite_inferior", "Limite_superior",
        "rc_Homem", "Limite_inf_Homem", "Limite_sup_Homem",
        "rc_Mulher", "Limite_inf_Mulher", "Limite_sup_Mulher",
        "rc_Publica", "Limite_inf_Publica", "Limite_sup_Publica",
        "rc_Privada", "Limite_inf_Privada", "Limite_sup_Privada"
    ]
    
    # Adicionar cabeçalhos
    for col_idx, cabecalho in enumerate(cabecalhos, 1):
        cell = ws_consolidado.cell(row=1, column=col_idx)
        cell.value = cabecalho
        cell.font = Font(bold=True, size=11, color="FFFFFF")
        cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    
    linha_atual = 2
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Processar cada arquivo
    for arquivo_name, tabela_origem, nome_metrica in arquivos:
        caminho = os.path.join(diretorio_origem, arquivo_name)
        
        if os.path.exists(caminho):
            try:
                wb = openpyxl.load_workbook(caminho, data_only=True)
                
                # Pegar a TERCEIRA aba (índice 2)
                if len(wb.worksheets) > 2:
                    ws = wb.worksheets[2]
                else:
                    print(f"⚠ {arquivo_name} não possui terceira aba, pulando...")
                    continue
                
                # Coletar todas as linhas de dados
                dados = []
                for row in ws.iter_rows(values_only=True):
                    dados.append(row)
                
                # Procurar por "Total" para encontrar início dos dados reais
                inicio_dados = 0
                for idx, row in enumerate(dados):
                    if row and "Total" in str(row[0]):
                        inicio_dados = idx
                        break
                
                # Processar dados da terceira aba (Municípios)
                for row_idx in range(inicio_dados, len(dados)):
                    row = dados[row_idx]
                    
                    if not row or all(cell is None for cell in row):
                        continue
                    
                    municipio = str(row[0]).strip() if row[0] else ""
                    
                    # Pular linhas de rodapé/fonte
                    if municipio.startswith("Fonte:"):
                        continue
                    
                    # Processar linhas com dados de municípios
                    if municipio:
                        # Montar linha consolidada
                        nova_linha = [
                            tabela_origem,
                            nome_metrica,
                            municipio
                        ]
                        
                        # Adicionar valores (começando da coluna 1, pulando a coluna 0 que é o nome)
                        if len(row) > 1:
                            for col_idx in range(1, min(len(row), 17)):
                                valor = row[col_idx]
                                if isinstance(valor, (int, float)):
                                    nova_linha.append(round(valor, 2))
                                else:
                                    nova_linha.append(valor)
                        
                        # Preencher linhas faltantes
                        while len(nova_linha) < len(cabecalhos):
                            nova_linha.append(None)
                        
                        # Escrever linha no workbook consolidado
                        for col_idx, valor in enumerate(nova_linha[:len(cabecalhos)], 1):
                            cell = ws_consolidado.cell(row=linha_atual, column=col_idx)
                            cell.value = valor
                            cell.border = thin_border
                            cell.alignment = Alignment(wrap_text=True, vertical="center")
                            if col_idx > 3 and isinstance(valor, (int, float)):
                                cell.number_format = '0.00'
                        
                        linha_atual += 1
                
                wb.close()
                print(f"✓ {arquivo_name} (aba {ws.title}) processado")
            except Exception as e:
                print(f"✗ Erro em {arquivo_name}: {e}")
        else:
            print(f"✗ Arquivo não encontrado: {arquivo_name}")
    
    # Ajustar largura das colunas
    for col_idx in range(1, len(cabecalhos) + 1):
        col_letter = get_column_letter(col_idx)
        if col_idx <= 3:
            ws_consolidado.column_dimensions[col_letter].width = 30
        else:
            ws_consolidado.column_dimensions[col_letter].width = 15
    
    # Salvar arquivo
    output_path = os.path.join(diretorio_origem, "Tabelas_12_Consolidadas_Municipios.xlsx")
    wb_consolidado.save(output_path)
    print(f"\n✓ Arquivo consolidado salvo em: {output_path}")
    
    return output_path


if __name__ == "__main__":
    consolidar_tabelas_municipios()
