# Project Context Document: KitaStock Inventory & Business Intelligence Platform

## Executive Overview

-   **Project Name:** KitaStock
-   **Project Type:** SaaS / Progressive Web App (PWA)
-   **Industry/Domain:** Small Business Inventory Management & Business
    Intelligence
-   **Developer Role:** Full-Stack Developer
-   **Primary Tech Stack:** Next.js 16, FastAPI, PostgreSQL, TanStack
    Query, Dexie/IndexedDB, Shadcn UI, Bklit Charts
-   **Core Focus:** Inventory management, sales tracking, purchasing,
    online ordering, business insights, and AI-assisted decision support

------------------------------------------------------------------------

## 1. Problem Statement & Operational Bottlenecks

### A. Manual Inventory Management

Small business owners often rely on spreadsheets or manual records to
track products, stock levels, purchases, sales, and stock movements.
This makes it difficult to maintain an accurate view of inventory and
identify issues early.

### B. Limited Business Visibility

Traditional inventory tools often focus on recording transactions
without helping owners understand what the data means. Business owners
need a clearer view of sales performance, inventory value, demand
patterns, and potential stock issues.

### C. Fragmented Online Ordering

Small sellers may share product information through social media or
messaging platforms but lack a simple, dedicated product portal where
customers can browse available items and submit order requests.

### D. Connectivity Constraints

Small businesses may operate in locations with unreliable internet
connectivity. A web-based inventory system that requires a constant
connection can interrupt daily operations.

### E. Difficulty Turning Data Into Decisions

Raw sales and inventory data does not always tell an owner what action
to take. KitaStock provides AI-assisted explanations and recommendations
based on existing business data.

------------------------------------------------------------------------

## 2. Solutions & Technical Architecture

### A. Full-Stack Application Architecture

-   Built KitaStock as a full-stack application using **Next.js 16** for
    the frontend and **FastAPI** for backend services.
-   Used **PostgreSQL** as the primary relational database.
-   Designed business-scoped data structures so inventory, sales,
    purchases, orders, and AI usage remain isolated per business.
-   Implemented role-based access for business members and separate
    platform administration.

### B. Inventory & Sales Management

-   Built product and SKU management for tracking inventory.
-   Implemented sales, returns, purchases, receiving, suppliers, and
    stock adjustments.
-   Added inventory status and stock monitoring to help owners identify
    low stock, out-of-stock items, reorder risks, and other inventory
    conditions.
-   Designed dashboard and intelligence views around owner-oriented
    business questions rather than simply displaying raw metrics.

### C. Business Intelligence Dashboard

-   Built a business overview dashboard showing key business metrics
    such as revenue, gross profit, margin, inventory value, sales
    trends, online orders, and demand patterns.
-   Used **Bklit Charts** for data visualization.
-   Added historical demand-pattern visualization to help owners
    understand when customers buy the most.
-   Separated positive business-performance reporting from inventory
    issues and action-oriented inventory intelligence.

### D. AI-Assisted Business Intelligence

KitaStock uses AI to turn existing application data into understandable
business explanations and recommendations.

AI-assisted features include: - **Daily Inventory Briefing** ---
summarizes important business and inventory information. - **Demand
Forecasting** --- estimates future product demand using historical sales
and inventory information. - **Reorder Assistant** --- helps determine
what products may need to be reordered. - **Inventory Anomaly
Explanations** --- explains unusual stock movements or discrepancies and
suggests what to check. - **Ask KitaStock** --- allows owners to ask
natural-language questions about their business data. - **Report
Summaries** --- converts report metrics into concise, understandable
explanations.

The application performs deterministic calculations from business data
first, while AI is used primarily to explain those results in natural
language.

### E. Online Store & Customer Order Portal

-   Added a public-facing online store for each business.
-   Businesses can publish selected products through a shareable public
    link.
-   Customers can browse available products, select quantities, and
    submit order requests.
-   Businesses can view and manage incoming online orders from the owner
    dashboard.
-   Added QR-code sharing as another way for businesses to distribute
    their online store.
-   Designed the store URL as a reusable customer-facing portal rather
    than requiring sellers to create a new link for every order.

### F. Offline-First PWA Architecture

-   Implemented Progressive Web App capabilities for supported offline
    operations.
-   Used **Dexie/IndexedDB** for local persistence and a durable
    mutation outbox.
-   Used **TanStack Query** for server-state caching and
    synchronization.
-   Supported selected transactions while offline, with pending changes
    synchronized when connectivity returns.
-   Designed the service worker to handle application assets while
    keeping business API state under the application's data layer.
-   Preserved authentication through HTTP-only cookies rather than
    storing authentication tokens in local storage or IndexedDB.

### G. Authentication, Authorization & Business Isolation

-   Implemented HTTP-only cookie-based authentication.
-   Added business membership and role-based access.
-   Designed the system so a user can belong to multiple businesses
    while each business maintains its own subscription, inventory,
    orders, AI usage, and members.
-   Separated platform-level administration from business-level
    permissions.

### H. Subscription & Usage Model

-   Designed a tiered subscription structure for small businesses.
-   Free, Pro, and Business plans use business-level billing and limits.
-   Implemented weekly AI action allowances by business.
-   Added SKU and member limits based on subscription level.
-   Pro includes offline operations and the Weekly Owner Summary
    concept, while Business expands capacity and supports custom roles.
-   Designed manual subscription upgrade and approval workflows for the
    MVP without requiring an integrated payment gateway.

------------------------------------------------------------------------

## 3. Product Experience & UI/UX

### Owner-First Dashboard

The dashboard was designed around the question:

> **How is my business doing?**

It emphasizes: - Sales performance - Gross profit - Margin - Inventory
value - Sales trends - Online orders - Demand patterns - Business
updates

More operational issues are handled through the separate Inventory
Intelligence experience.

### Inventory Intelligence

The Inventory Intelligence experience focuses on:

> **What needs attention, why, and what should I do?**

It surfaces: - Low stock - Out-of-stock risks - Reorder-point issues -
Stock discrepancies - Demand-related risks - AI-generated explanations -
Suggested actions

This separation keeps the main dashboard focused on business progress
while giving inventory problems their own action-oriented workspace.

### Responsive Experience

-   Designed responsive layouts for desktop and mobile.
-   Included mobile navigation and mobile-friendly business intelligence
    views.
-   Designed the customer-facing online store separately from the
    authenticated owner workspace.

------------------------------------------------------------------------

## 4. Key Business Impact

### Improved Inventory Visibility

KitaStock gives small business owners a centralized view of products,
stock movements, purchases, sales, inventory value, and stock
conditions.

### Faster Business Understanding

Instead of requiring owners to interpret multiple charts and tables
themselves, AI-assisted briefings and explanations summarize important
business information in plain language.

### Better Reordering Decisions

Historical sales, available stock, incoming inventory, supplier lead
time, and demand information can be used to support reorder decisions.

### Simplified Online Selling

The public online store gives small sellers a lightweight way to publish
products and receive customer order requests through a shareable link or
QR code.

### Continued Operations During Connectivity Issues

The PWA and offline data architecture allow supported inventory
operations to continue during temporary connectivity loss and
synchronize pending changes when the connection returns.

------------------------------------------------------------------------

## 5. Technology Stack

  Area              Technology
  ----------------- ----------------------------
  Frontend          Next.js 16
  Backend           FastAPI
  Database          PostgreSQL
  Server State      TanStack Query
  Offline Storage   Dexie / IndexedDB
  UI                Shadcn UI
  Charts            Bklit Charts
  Authentication    HTTP-only cookies
  PWA               Service Worker + IndexedDB
  AI                Gemini
  Architecture      Full-stack SaaS / PWA

------------------------------------------------------------------------

## 6. Vector Retrieval QA Pairs (Context Hints for Portfolio AI)

### Q: What is KitaStock?

KitaStock is a small-business inventory and business intelligence
platform that combines inventory management, sales, purchasing, online
ordering, business dashboards, AI-assisted insights, and offline-capable
operations in one application.

### Q: What was Renzo's role on the KitaStock project?

Renzo designed and developed KitaStock as a full-stack application,
working across the Next.js frontend, FastAPI backend, PostgreSQL data
layer, authentication, offline architecture, business intelligence
dashboards, AI-assisted features, and customer-facing online store.

### Q: What tech stack was used to build KitaStock?

KitaStock uses Next.js 16 for the frontend, FastAPI for backend
services, PostgreSQL for data storage, TanStack Query for server-state
management, Dexie/IndexedDB for offline persistence, Shadcn UI for
interface components, and Bklit Charts for data visualization.

### Q: How does KitaStock handle inventory management?

KitaStock provides product and SKU management, stock tracking, stock
adjustments, sales, returns, purchases, receiving, suppliers, inventory
valuation, reorder monitoring, and inventory intelligence features.

### Q: How does KitaStock use AI?

KitaStock uses AI to explain and summarize business data that has
already been calculated by the application. Features include Daily
Inventory Briefing, Demand Forecasting, Reorder Assistant, Inventory
Anomaly Explanations, and AI-generated report summaries.

### Q: What is the purpose of the Daily Inventory Briefing?

The Daily Inventory Briefing provides a concise summary of important
business and inventory information, highlighting what happened, what
needs attention, and what the owner may want to do next.

### Q: What is KitaStock's Demand Forecasting feature?

Demand Forecasting uses historical sales and inventory information to
estimate future product demand and help owners plan upcoming purchases
and reorder quantities.

### Q: What is Inventory Intelligence in KitaStock?

Inventory Intelligence is the action-oriented part of KitaStock that
helps owners identify stock issues, understand possible causes, and
determine what to check or do next.

### Q: Does KitaStock support an online store?

Yes. Each business can have a public online store where selected
products can be published. Customers can browse products, choose
quantities, and submit order requests through a shareable link or QR
code.

### Q: How does the KitaStock online store work?

A business publishes selected products to its public store. The business
shares the permanent store link or QR code with customers. Customers
browse the products, select quantities, and submit an order request. The
owner can then review and manage those orders from the KitaStock
dashboard.

### Q: Does KitaStock support offline operations?

Yes. KitaStock is designed as a Progressive Web App and uses
Dexie/IndexedDB for local persistence and a durable mutation outbox.
Supported transactions can be saved locally while offline and
synchronized when connectivity returns.

### Q: How does KitaStock handle authentication?

KitaStock uses HTTP-only cookies for authentication. Authentication
tokens are not stored in local storage or IndexedDB.

### Q: How is data separated between businesses?

Business data is scoped by business membership and business identifiers.
Products, sales, purchases, inventory, orders, AI usage, subscriptions,
and offline records are associated with the appropriate business.

### Q: What makes KitaStock different from a basic inventory system?

KitaStock combines inventory operations with business intelligence,
AI-assisted explanations, demand analysis, offline-capable workflows,
and a customer-facing online store. The goal is not only to record stock
movements but also to help owners understand their business and decide
what to do next.

### Q: Who is KitaStock designed for?

KitaStock is designed primarily for small business owners and online
sellers who need a simple way to manage inventory, sales, purchasing,
customer orders, and business information without requiring specialized
inventory or data-analysis expertise.

### Q: What is the main product idea behind KitaStock?

The product name reflects two Filipino meanings of "kita": earnings and
seeing/visibility. KitaStock is built around the idea of helping
business owners see their stock and see the business activity that
drives their earnings.
