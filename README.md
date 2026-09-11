# Resume RAG & AI Job Matching Agent

An AI-powered Resume Retrieval-Augmented Generation (RAG) and Job Matching system that processes resumes, generates semantic embeddings, stores them in a vector database, and intelligently matches candidates against job descriptions.

The project evolves a traditional Resume RAG pipeline into a conversational AI recruitment agent using LangGraph, LLMs, semantic search, hybrid candidate scoring, human feedback, and multi-round candidate screening.

---

## Project Overview

This project combines Resume RAG with an AI-powered recruitment agent.

The system can:

- Load and process resume documents
- Split resumes into meaningful sections
- Extract candidate metadata
- Generate semantic embeddings
- Store embeddings in ChromaDB
- Perform semantic similarity search
- Perform hybrid semantic + keyword matching
- Filter candidates based on required experience
- Match critical technical skills
- Rank candidates on a 0-100 scale
- Provide match reasoning
- Provide relevant resume excerpts
- Extract job requirements using an LLM
- Separate must-have and nice-to-have requirements
- Compare candidates head-to-head
- Generate candidate-specific interview questions
- Generate recruiter-friendly screening reports
- Accept recruiter feedback
- Re-rank candidates based on recruiter preferences
- Track ranking changes after feedback
- Perform deep candidate screening
- Generate final HIRE / NO HIRE decisions
- Support natural-language recruiter queries
- Evaluate retrieval performance
- Run automated tests

---

# Key Features

## 1. Resume RAG Pipeline

The system processes resumes through a complete RAG pipeline:

```text
Resume Files
     |
     v
File Processing
     |
     v
Resume Chunking
     |
     v
Metadata Extraction
     |
     v
Embedding Generation
     |
     v
ChromaDB
     |
     v
Semantic Search

  ---
  ##SYSTEM ARCHITECTURE

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
                    ChromaDB Vector DB
                              |
                              |
                              |
                     Job Description Input
                              |
                              v
                    Requirement Extraction
                         (LLM + Rules)
                              |
                              v
                    Semantic Vector Search
                              |
                              v
                     Candidate Retrieval
                              |
                              v
                    Hybrid Candidate Scoring
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
         Skill Score    Experience Score   Semantic Score
              |               |               |
              +---------------+---------------+
                              |
                              v
                         Domain Score
                              |
                              v
                        Top-K Ranking
                              |
                              v
                    Screening Report
                              |
                              v
                       Human Feedback
                              |
                    +---------+---------+
                    |                   |
               No Feedback          Feedback
                    |                   |
                    v                   v
              Deep Screening      Apply Feedback
                    |                   |
                    |                   v
                    |             Re-run Matching
                    |                   |
                    +---------<---------+
                              |
                              v
                     Final HIRE / NO HIRE
                              |
                              v
                             END

---
###LANG GRAPH AGENT WORK FLOW

START
  |
  v
Parse JD
  |
  v
Extract Requirements
  |
  v
Search Resumes
  |
  v
Rank Candidates
  |
  v
Generate Screening Report
  |
  v
Human Feedback
  |
  +----------------------+
  |                      |
  | No Feedback          | Feedback
  |                      |
  v                      v
Deep Screening      Apply Feedback
  |                      |
  v                      v
Final Decision      Re-run Matching
  |                      |
  v                      |
 END <-------------------+