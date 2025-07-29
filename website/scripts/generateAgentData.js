const fs = require('fs');
const path = require('path');

// Parse YAML frontmatter from markdown files
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);
  
  if (!match) {
    return { frontmatter: {}, content: content };
  }
  
  const frontmatterText = match[1];
  const markdownContent = match[2];
  
  // Simple YAML parser for our needs
  const frontmatter = {};
  const lines = frontmatterText.split('\n');
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();
      
      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) || 
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      
      // Handle arrays (tools)
      if (key === 'tools' && value.includes(',')) {
        frontmatter[key] = value.split(',').map(tool => tool.trim());
      } else {
        frontmatter[key] = value;
      }
    }
  }
  
  return { frontmatter, content: markdownContent };
}

// Extract sections from markdown content
function extractSections(content) {
  const sections = {};
  const lines = content.split('\n');
  let currentSection = null;
  let currentContent = [];
  
  for (const line of lines) {
    if (line.startsWith('## ')) {
      // Save previous section
      if (currentSection) {
        sections[currentSection] = currentContent.join('\n').trim();
      }
      
      // Start new section
      currentSection = line.replace('## ', '').trim();
      currentContent = [];
    } else if (currentSection) {
      currentContent.push(line);
    }
  }
  
  // Save last section
  if (currentSection) {
    sections[currentSection] = currentContent.join('\n').trim();
  }
  
  return sections;
}

// Extract workflow examples from content
function extractWorkflows(content) {
  const workflows = [];
  const workflowRegex = /### (.+?)\n([\s\S]*?)(?=\n### |\n## |$)/g;
  let match;
  
  while ((match = workflowRegex.exec(content)) !== null) {
    workflows.push({
      title: match[1].trim(),
      description: match[2].trim().split('\n')[0] || match[1].trim()
    });
  }
  
  return workflows;
}

// Generate agent categories based on agent names and descriptions
function categorizeAgent(name, description) {
  const categoryMap = {
    'data-io': {
      name: 'Data I/O',
      icon: '💾',
      description: 'Scientific data formats and I/O operations'
    },
    'analysis-viz': {
      name: 'Analysis & Visualization', 
      icon: '📊',
      description: 'Data analysis and visualization'
    },
    'hpc-performance': {
      name: 'HPC & Performance',
      icon: '🚀',
      description: 'High-performance computing and optimization'
    },
    'research-doc': {
      name: 'Research & Documentation',
      icon: '📚',
      description: 'Research literature and documentation'
    },
    'workflow': {
      name: 'Workflow Management',
      icon: '⚙️',
      description: 'Workflow orchestration and environment management'
    }
  };
  
  // Map agent names to categories
  if (name.includes('data-io')) return categoryMap['data-io'];
  if (name.includes('analysis') || name.includes('viz')) return categoryMap['analysis-viz'];
  if (name.includes('hpc') || name.includes('performance')) return categoryMap['hpc-performance'];
  if (name.includes('research') || name.includes('doc')) return categoryMap['research-doc'];
  if (name.includes('workflow') || name.includes('orchestrator')) return categoryMap['workflow'];
  
  // Default category
  return {
    name: 'General',
    icon: '🤖',
    description: 'General purpose AI agent'
  };
}

// Main function to generate agent data
function generateAgentData() {
  const agentsDir = path.join(__dirname, '../../agents');
  const outputFile = path.join(__dirname, '../src/data/agentData.js');
  
  if (!fs.existsSync(agentsDir)) {
    console.error('Agents directory not found:', agentsDir);
    return;
  }
  
  const agents = {};
  const categories = new Set();
  
  // Read all .md files from agents directory
  const files = fs.readdirSync(agentsDir).filter(file => file.endsWith('.md'));
  
  for (const file of files) {
    const filePath = path.join(agentsDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const { frontmatter, content: markdownContent } = parseFrontmatter(content);
    
    if (!frontmatter.name) {
      console.warn(`Skipping ${file}: no name in frontmatter`);
      continue;
    }
    
    const sections = extractSections(markdownContent);
    const category = categorizeAgent(frontmatter.name, frontmatter.description);
    const workflows = extractWorkflows(sections['Common Workflows'] || '');
    
    categories.add(JSON.stringify(category));
    
    agents[frontmatter.name] = {
      name: frontmatter.name,
      displayName: frontmatter.name.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' '),
      description: frontmatter.description,
      category: category.name,
      categoryData: category,
      tools: frontmatter.tools || [],
      expertise: extractListItems(sections['Core Expertise'] || ''),
      bestPractices: extractListItems(sections['Best Practices'] || ''),
      workflows: workflows,
      slug: frontmatter.name,
      filename: file,
      lastModified: fs.statSync(filePath).mtime.toISOString()
    };
  }
  
  // Convert categories set back to object
  const categoryData = {};
  for (const categoryStr of categories) {
    const category = JSON.parse(categoryStr);
    categoryData[category.name.toLowerCase().replace(/\s+/g, '-')] = category;
  }
  
  // Generate the output file
  const outputContent = `// Auto-generated agent data
// DO NOT EDIT - Run npm run generate-agents to update

export const agentData = ${JSON.stringify(agents, null, 2)};

export const categories = ${JSON.stringify(categoryData, null, 2)};

export const agentStats = {
  total: ${Object.keys(agents).length},
  categories: ${Object.keys(categoryData).length},
  lastGenerated: '${new Date().toISOString()}'
};
`;
  
  // Ensure output directory exists
  fs.mkdirSync(path.dirname(outputFile), { recursive: true });
  fs.writeFileSync(outputFile, outputContent);
  
  console.log(`Generated agent data for ${Object.keys(agents).length} agents`);
  console.log(`Categories: ${Object.keys(categoryData).join(', ')}`);
}

// Helper function to extract list items from markdown
function extractListItems(content) {
  const items = [];
  const lines = content.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      items.push(trimmed.substring(2).replace(/^\*\*(.+?)\*\*:?\s*/, '$1: '));
    }
  }
  
  return items;
}

// Run if called directly
if (require.main === module) {
  generateAgentData();
}

module.exports = { generateAgentData };