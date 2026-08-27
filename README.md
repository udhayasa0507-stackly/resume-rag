# Resume RAG & Job Matching System

An AI-powered Resume Retrieval-Augmented Generation (RAG) system that
processes resumes, generates semantic embeddings, stores them in a vector
database, and matches candidates against job descriptions using semantic
search, keyword matching, metadata filtering, and candidate scoring.

---

## Project Overview

This project implements a Resume RAG and Job Matching Engine.

The system can:

- Load and process resume documents
- Split resumes into meaningful sections
- Extract candidate metadata
- Generate semantic embeddings
- Store embeddings in ChromaDB
- Perform semantic similarity search
- Perform hybrid semantic + keyword matching
- Filter candidates based on required experience
- Match critical skills
- Rank candidates on a 0-100 scale
- Provide match reasoning and relevant resume excerpts
- Evaluate retrieval performance
- Measure search latency

---

## Architecture

```text
                    Resume Files
                         |
                         v
                 File Processing
                         |
                         v
                Intelligent Chunking
                         |
                         v
                Metadata Extraction
                         |
                         v
              Sentence Transformer
              all-MiniLM-L6-v2
                         |
                         v
                    Embeddings
                         |
                         v
                    ChromaDB
                  Vector Database
                         |
                         |
              Job Description Input
                         |
                         v
                 Job Embedding
                         |
                         v
             Semantic Vector Search
                         |
                         +
                  Keyword Matching
                         |
                         v
              Must-Have Filtering
                         |
                         v
                Candidate Scoring
                         |
                         v
                   Top-K Ranking
                         |
                         v
              Match Reasoning Output