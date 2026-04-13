function ResultItem({ title, summary, tag }) {
  return (
    <article className="result-item">
      <h4>{title}</h4>
      <p>{summary}</p>
      <span>{tag}</span>
    </article>
  );
}

export default ResultItem;
