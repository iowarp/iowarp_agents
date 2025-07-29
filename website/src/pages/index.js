import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import AgentShowcase from '@site/src/components/AgentShowcase';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Specialized AI subagents for scientific computing workflows.">
      <main>
        <AgentShowcase />
      </main>
    </Layout>
  );
}
