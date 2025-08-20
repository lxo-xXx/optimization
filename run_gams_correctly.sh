#!/bin/bash

echo "=========================================="
echo "Heat Recovery Process Optimization - GAMS"
echo "=========================================="
echo ""

echo "🚀 Running CORRECTED GAMS files..."
echo ""

echo "✅ Running Configuration A (Simple ORC)..."
gams orc_standalone_config_a.gms
echo ""

echo "✅ Running Configuration B (ORC with Recuperator)..."
gams orc_standalone_config_b.gms
echo ""

echo "✅ Running Complete Analysis (Both Configurations)..."
gams run_both_configurations.gms
echo ""

echo "✅ Running Distinct Variant: Environmentally-Aware Multi-Objective ORC..."
gams orc_env_multiobjective.gms
echo ""

echo "=========================================="
echo "IMPORTANT: Do NOT run these broken files:"
echo "❌ run_optimization.gms"
echo "❌ orc_enhanced_config_a.gms" 
echo "❌ orc_config_b.gms"
echo ""
echo "✅ ONLY use these corrected files:"
echo "✅ orc_standalone_config_a.gms"
echo "✅ orc_standalone_config_b.gms"
echo "✅ run_both_configurations.gms"
echo "✅ orc_env_multiobjective.gms (distinct variant)"
echo "=========================================="