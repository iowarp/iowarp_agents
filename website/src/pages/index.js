import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import AgentShowcase from '@site/src/components/AgentShowcase';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Specialized AI subagents for scientific computing workflows. Built for Claude Code, designed to be adaptable as other systems develop similar capabilities.">
      <main>
        <AgentShowcase />
      </main>
    </Layout>
  );
}
