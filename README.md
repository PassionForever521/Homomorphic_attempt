This is a homomorphic encryption attempt, encrypting the embedded information (SEAL) and then creating a socket

# 🔒 Homomorphic_attempt

A minimal but functional prototype for **secure vector similarity computation** using **homomorphic encryption (CKKS)** and **socket-based communication** between two parties (A and B).

## 🚀 Project Overview

This project demonstrates how two parties can compute cosine similarity between their embeddings **without revealing the actual vectors**.

- ✅ Embeddings are encrypted using [TenSEAL (CKKS scheme)](https://github.com/OpenMined/TenSEAL)
- ✅ Random masking is applied to prevent reverse-engineering
- ✅ Communication is done via socket (TCP/IP)
- ✅ Only **similarity result** or partial information (like dot product) is shared — no raw vectors

---

## 📦 Structure

```bash
.
├── main_A.py          # Party A sends encrypted masked embedding
├── main_B.py          # Party B receives, decrypts, and evaluates similarity
├── party.py           # Logic for both PartyA and PartyB
├── llm.py             # (Optional) For real embeddings via sentence-transformers
├── graph.py           # (Optional) Simple entity/vertex structure
├── config.py          # (Optional) Parameters like sigma, port
└── README.md          # You're here.
