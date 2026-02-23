-- ============================================================
-- consultas_sql.sql
-- Consultas SQL sobre as vendas dos produtos Quod (2023)
-- Tabela base: data_clean (gerada pelos scripts Python)
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- CONSULTA 1
-- Produto, categoria e soma total de vendas (Quantidade × Preço)
-- Ordenado por valor total de vendas de forma decrescente
-- ────────────────────────────────────────────────────────────
-- Lógica: agrupa por Produto e Categoria (1-para-1 neste dataset),
-- calcula a receita total somando Quantidade × Preço para cada linha
-- e ordena do maior para o menor, permitindo identificar rapidamente
-- quais produtos geram mais receita para a Quod.
-- ────────────────────────────────────────────────────────────

SELECT
    Produto,
    Categoria,
    SUM(Quantidade * Preço)        AS Total_Vendas,
    SUM(Quantidade)                AS Total_Consultas,
    COUNT(*)                       AS Qtd_Transacoes,
    ROUND(AVG(Quantidade * Preço), 2) AS Ticket_Medio
FROM data_clean
GROUP BY
    Produto,
    Categoria
ORDER BY
    Total_Vendas DESC;


-- ────────────────────────────────────────────────────────────
-- CONSULTA 2
-- Produtos que MENOS venderam em junho de 2023
-- (o enunciado menciona jun/2024, mas o dataset cobre 2023;
--  a lógica é idêntica — filtra pelo mês 6 do ano disponível)
-- ────────────────────────────────────────────────────────────
-- Lógica: filtra o período de junho, agrega total de vendas por produto
-- e ordena em ordem crescente para expor os de menor desempenho.
-- O uso de HAVING garante que só produtos com ao menos uma venda
-- no período sejam exibidos (evita artefatos de LEFT JOIN).
-- ────────────────────────────────────────────────────────────

SELECT
    Produto,
    Categoria,
    SUM(Quantidade * Preço) AS Total_Vendas_Junho,
    SUM(Quantidade)          AS Total_Consultas_Junho,
    COUNT(*)                 AS Qtd_Transacoes_Junho
FROM data_clean
WHERE
    strftime('%Y', Data) = '2023'   -- adapte para '2024' quando houver dados
    AND strftime('%m', Data) = '06' -- mês de junho
GROUP BY
    Produto,
    Categoria
HAVING
    Total_Vendas_Junho > 0
ORDER BY
    Total_Vendas_Junho ASC;         -- menor venda primeiro


-- ────────────────────────────────────────────────────────────
-- CONSULTA BÔNUS
-- Evolução mensal de receita por categoria — útil para
-- identificar sazonalidade e planejar campanhas comerciais
-- ────────────────────────────────────────────────────────────

SELECT
    strftime('%Y-%m', Data)          AS Ano_Mes,
    Categoria,
    SUM(Quantidade * Preço)          AS Receita_Mensal,
    SUM(Quantidade)                  AS Consultas_Mensais
FROM data_clean
GROUP BY
    Ano_Mes,
    Categoria
ORDER BY
    Ano_Mes,
    Receita_Mensal DESC;
