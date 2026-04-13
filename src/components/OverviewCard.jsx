function OverviewCard({ label, value, sub }) {
  return (
    <article className="overview-card">
      <p>{label}</p>
      <strong>{value}</strong>
      <span>{sub}</span>
    </article>
  );
}

export default OverviewCard;
