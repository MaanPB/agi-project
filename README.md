# AGI Project - Modular AI System

A step-by-step implementation of an AGI-like system with retrieval, tools, planners, memory, multimodal perception, continual learning, and safety features.

## 🎯 Project Goals

Build a modular, extensible system that progressively behaves like a generalist agent by composing:
- Retrieval-augmented generation (RAG)
- Tool use and planning
- Long-term memory (vector DB + knowledge graph)
- Multimodal perception (vision + audio)
- Continual learning (without catastrophic forgetting)
- Safety and governance

## 📋 Current Status

**Phase 0: Foundation & Environment** ✅ (Complete)
- Repository structure created
- Configuration management
- Structured logging
- Utility functions
- Unit tests

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- 8GB+ RAM recommended

### Setup

```bash
# Clone or navigate to the project
cd agi_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run the demo
python -m src.agi_core.main
```

## 📁 Project Structure

```
agi_project/
├── src/
│   └── agi_core/
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       ├── logger.py          # Structured JSON logging
│       ├── utils.py           # Utility functions
│       └── main.py            # Entry point
├── tests/
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── data/                      # Data storage
├── models/                    # Saved models
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentation
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/unit/test_config.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 📚 Development Phases

- [x] Phase 0: Foundation & Environment
- [ ] Phase 1: Core ML Skills & Model Scaffolding
- [ ] Phase 2: Retrieval Memory (Vector DB)
- [ ] Phase 3: Tool Kit & Agent Loop
- [ ] Phase 4: Knowledge Graph & Neurosymbolic Bridge
- [ ] Phase 5: Continual Learning & Memory Consolidation
- [ ] Phase 6: Reflection & Self-Improvement Loop
- [ ] Phase 7: Multimodal Perception
- [ ] Phase 8: Planner Upgrade & Learned Policies
- [ ] Phase 9: Safety, PII & Governance
- [ ] Phase 10: Evaluation, Metrics & CI
- [ ] Phase 11: Deployment & Scaling
- [ ] Phase 12: Research Loop & Governance

## 🤝 Contributing

This is a learning project. Feel free to experiment and modify!

## 📄 License

MIT License - See LICENSE file for details

## 🔒 Ethics & Safety

- Always obey local laws and privacy regulations (GDPR/CCPA)
- Never ingest private data without explicit consent
- Build logging, consent flows, and red-team testing into every phase
- PII detection and safety guardrails are mandatory

## 📖 Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [NetworkX Documentation](https://networkx.org/)
