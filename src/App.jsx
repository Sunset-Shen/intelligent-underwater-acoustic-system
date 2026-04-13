import {
  AudioLines,
  Bot,
  Database,
  Gauge,
  Layers,
  ShieldCheck,
  Sparkles,
  Workflow,
} from 'lucide-react';
import { useState } from 'react';
import FunctionCard from './components/FunctionCard';
import OverviewCard from './components/OverviewCard';
import ResultItem from './components/ResultItem';

const flowSteps = [
  '数据接入与预处理',
  '可解释生成与增强',
  '轻量识别训练/推理',
  '结果输出与管理',
];

const featureCards = [
  {
    icon: Database,
    title: '数据管理',
    description: '统一管理多源水声数据集与标注版本。',
  },
  {
    icon: Sparkles,
    title: '可解释生成',
    description: '面向目标特征约束的可解释增强流程。',
  },
  {
    icon: Bot,
    title: '轻量识别',
    description: '低成本部署导向的识别训练与推理。',
  },
  {
    icon: Layers,
    title: '结果中心',
    description: '汇总任务结果、日志与导出记录。',
  },
];

const overviewData = [
  { label: '支持的数据集', value: '12 套', sub: '含公开集与内部采集集' },
  { label: '生成增强模块', value: '4 项', sub: '时频扰动 / 条件生成 / 质量评估' },
  { label: '识别模型', value: '6 个', sub: 'CNN / Transformer / 轻量混合结构' },
  { label: '当前运行模式', value: '原型验证', sub: 'Mock 数据与流程联调' },
];

const recentResults = [
  {
    title: '最近一次识别结果',
    summary: '近岸噪声场景下目标类别 T-03，置信度 93.4%。',
    tag: '识别任务 #R20260413-01',
  },
  {
    title: '最近一次增强任务',
    summary: '完成 3,200 条样本增强，质量评估等级 A。',
    tag: '增强任务 #G20260412-06',
  },
  {
    title: '最近一次模型运行摘要',
    summary: '轻量模型 LAM-Net 推理延时 18ms，稳定运行。',
    tag: '运行记录 #M20260412-09',
  },
];

function App() {
  const [placeholder, setPlaceholder] = useState('点击上方功能卡片查看占位内容。');

  return (
    <div className="app-shell">
      <header className="top-nav">
        <div>
          <h1>智能水声数据生成及轻量化识别系统</h1>
          <p>面向水声目标识别的生成增强与轻量识别一体化原型系统</p>
        </div>
        <div className="status-panel">
          <ShieldCheck size={16} />
          <span>系统状态：稳定</span>
        </div>
      </header>

      <main className="main-content">
        <section className="hero-section card-surface">
          <div>
            <h2>水声智能处理一体化工作台</h2>
            <p>
              聚焦“数据 — 生成 — 识别 — 管理”全流程，提供清晰、可扩展、面向研究落地的统一主界面。
            </p>
          </div>
          <div className="flow-wrapper">
            {flowSteps.map((step, idx) => (
              <div key={step} className="flow-step">
                <span>{idx + 1}</span>
                <strong>{step}</strong>
                {idx !== flowSteps.length - 1 && <Workflow size={16} />}
              </div>
            ))}
          </div>
        </section>

        <section className="feature-grid">
          {featureCards.map((card) => (
            <FunctionCard
              key={card.title}
              {...card}
              onClick={() => setPlaceholder(`${card.title}模块即将完善，当前为原型占位页。`)}
            />
          ))}
        </section>

        <section className="placeholder card-surface">
          <Gauge size={18} />
          <p>{placeholder}</p>
        </section>

        <section className="overview-section card-surface">
          <h3>
            <AudioLines size={18} /> 系统概览
          </h3>
          <div className="overview-grid">
            {overviewData.map((item) => (
              <OverviewCard key={item.label} {...item} />
            ))}
          </div>
        </section>

        <section className="results-section card-surface">
          <h3>最近结果预览</h3>
          <div className="results-list">
            {recentResults.map((item) => (
              <ResultItem key={item.title} {...item} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
