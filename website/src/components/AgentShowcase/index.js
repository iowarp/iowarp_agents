import React, { useState, useMemo } from 'react';
import Link from '@docusaurus/Link';
import { agentData, categories, agentStats } from '../../data/agentData';
import styles from './styles.module.css';

// Category filter component
const CategoryFilter = ({ activeCategory, onCategoryChange }) => {
  const categoryList = [
    { key: 'all', name: 'All Agents', icon: '🤖' },
    ...Object.entries(categories).map(([key, data]) => ({ key, ...data }))
  ];

  return (
    <div className={styles.categoryFilter}>
      {categoryList.map(({ key, name, icon }) => (
        <button
          key={key}
          className={`${styles.categoryButton} ${
            activeCategory === key ? styles.active : ''
          }`}
          onClick={() => onCategoryChange(key)}
        >
          <span className={styles.categoryIcon}>{icon}</span>
          {name}
        </button>
      ))}
    </div>
  );
};

// Search component
const SearchBar = ({ searchTerm, onSearchChange }) => {
  return (
    <div className={styles.searchContainer}>
      <input
        type="text"
        placeholder="Search agents..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        className={styles.searchInput}
      />
      <span className={styles.searchIcon}>🔍</span>
    </div>
  );
};

// Tools display component
const ToolsList = ({ tools, onShowMore }) => {
  const displayTools = tools.slice(0, 4); // Show first 4 tools
  const hasMore = tools.length > 4;

  return (
    <div className={styles.toolsList}>
      {displayTools.map((tool, index) => (
        <span key={index} className={styles.toolTag}>
          {tool}
        </span>
      ))}
      {hasMore && (
        <span 
          className={`${styles.toolTag} ${styles.moreTools} ${styles.clickableText}`}
          onClick={() => onShowMore('tools', tools)}
        >
          +{tools.length - 4} more
        </span>
      )}
    </div>
  );
};

// Modal component
const Modal = ({ isOpen, onClose, title, content, type }) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={handleOverlayClick}>
      <div className={styles.modalContent}>
        <div className={styles.modalHeader}>
          <h2 className={styles.modalTitle}>{title}</h2>
          <button className={styles.modalClose} onClick={onClose}>
            ✕
          </button>
        </div>
        
        {type === 'tools' && (
          <div className={styles.modalSection}>
            <h3>🛠️ Available Tools</h3>
            <div className={styles.modalToolsGrid}>
              {content.map((tool, index) => (
                <div key={index} className={styles.modalToolTag}>
                  {tool}
                </div>
              ))}
            </div>
          </div>
        )}
        
        {type === 'expertise' && (
          <div className={styles.modalSection}>
            <h3>🎯 Areas of Expertise</h3>
            <ul className={styles.modalList}>
              {content.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

// Individual agent card component
const AgentCard = ({ agentId, agent, onShowModal }) => {
  return (
    <div className={styles.agentCard}>
      <div className={styles.agentCardHeader}>
        <div className={styles.agentIcon}>{agent.categoryData.icon}</div>
        <div className={styles.agentCardInfo}>
          <h3 className={styles.agentName}>{agent.displayName}</h3>
          <span className={styles.agentCategory}>{agent.category}</span>
        </div>
      </div>
      
      <p className={styles.agentDescription}>{agent.description}</p>
      
      <div className={styles.agentDetails}>
        <div className={styles.expertisePreview}>
          <strong>Key Expertise:</strong>
          <ul className={styles.expertiseList}>
            {agent.expertise.slice(0, 3).map((item, index) => (
              <li key={index}>{item}</li>
            ))}
            {agent.expertise.length > 3 && (
              <li 
                className={`${styles.moreItems} ${styles.clickableText}`}
                onClick={() => onShowModal('expertise', agent.expertise, `${agent.displayName} - Areas of Expertise`)}
              >
                +{agent.expertise.length - 3} more areas
              </li>
            )}
          </ul>
        </div>
      </div>

      <div className={styles.agentFooter}>
        <ToolsList 
          tools={agent.tools} 
          onShowMore={(type, content) => onShowModal(type, content, `${agent.displayName} - Available Tools`)}
        />
        <div className={styles.agentActions}>
          <a
            href={`https://github.com/iowarp/iowarp_agents/blob/main/agents/${agent.filename}`}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.viewAgentButton}
          >
            View Source →
          </a>
        </div>
      </div>
    </div>
  );
};

// Stats component
const StatsBar = ({ totalAgents, filteredCount, activeCategory }) => {
  return (
    <div className={styles.statsBar}>
      <div className={styles.statsLeft}>
        <span className={styles.agentCount}>
          Showing {filteredCount} of {totalAgents} agents
          {activeCategory !== 'all' && (
            <span className={styles.categoryFilter}>
              in {categories[activeCategory]?.name || activeCategory}
            </span>
          )}
        </span>
      </div>
      <div className={styles.statsRight}>
        <span className={styles.lastUpdated}>
          Last updated: {new Date(agentStats.lastGenerated).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
};

// Main showcase component
const AgentShowcase = () => {
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [modalState, setModalState] = useState({
    isOpen: false,
    type: null,
    content: null,
    title: ''
  });

  // Filter agents based on category and search term
  const filteredAgents = useMemo(() => {
    let filtered = Object.entries(agentData);

    // Filter by category
    if (activeCategory !== 'all') {
      const categoryName = categories[activeCategory]?.name;
      if (categoryName) {
        filtered = filtered.filter(([_, agent]) => agent.category === categoryName);
      }
    }

    // Filter by search term
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(([_, agent]) =>
        agent.displayName.toLowerCase().includes(searchLower) ||
        agent.description.toLowerCase().includes(searchLower) ||
        agent.category.toLowerCase().includes(searchLower) ||
        agent.expertise.some(item => item.toLowerCase().includes(searchLower))
      );
    }

    return filtered;
  }, [activeCategory, searchTerm]);

  const handleShowModal = (type, content, title) => {
    setModalState({
      isOpen: true,
      type,
      content,
      title
    });
  };

  const handleCloseModal = () => {
    setModalState({
      isOpen: false,
      type: null,
      content: null,
      title: ''
    });
  };

  return (
    <div className={styles.showcase}>
      {/* Hero Section */}
      <div className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.title}>
            IOWarp Agents
            <span className={styles.badge}>{agentStats.total} Agents</span>
          </h1>
          <p className={styles.subtitle}>
            Specialized AI subagents for scientific computing workflows.
            Built for Claude Code, designed to be adaptable as other systems develop similar capabilities.
          </p>
        </div>
      </div>

      {/* Controls */}
      <div className={styles.controls}>
        <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
        <CategoryFilter
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
        />
      </div>

      {/* Stats */}
      <StatsBar
        totalAgents={agentStats.total}
        filteredCount={filteredAgents.length}
        activeCategory={activeCategory}
      />

      {/* Agent Grid */}
      <div className={styles.agentGrid}>
        {filteredAgents.length > 0 ? (
          filteredAgents.map(([agentId, agent]) => (
            <AgentCard 
              key={agentId} 
              agentId={agentId} 
              agent={agent} 
              onShowModal={handleShowModal}
            />
          ))
        ) : (
          <div className={styles.noResults}>
            <div className={styles.noResultsIcon}>🔍</div>
            <h3>No agents found</h3>
            <p>Try adjusting your search terms or category filter.</p>
          </div>
        )}
      </div>

      {/* Modal */}
      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={modalState.title}
        content={modalState.content}
        type={modalState.type}
      />

      {/* Quick Start Section */}
      <div className={styles.quickStart}>
        <h2>Quick Start</h2>
        <div className={styles.quickStartGrid}>
          <div className={styles.quickStartCard}>
            <h3>📋 Project Setup</h3>
            <pre className={styles.codeBlock}>
{`# Clone the repository
git clone https://github.com/iowarp/iowarp_agents.git

# Copy agents to your project
mkdir -p .claude/agents
cp iowarp_agents/agents/*.md .claude/agents/`}
            </pre>
          </div>
          <div className={styles.quickStartCard}>
            <h3>🚀 Usage</h3>
            <pre className={styles.codeBlock}>
{`# In Claude Code, use:
/agents

# Or natural language:
"Use the data-io-expert to help me convert this HDF5 file"`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentShowcase;