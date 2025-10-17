import "./ProductCard.css";

export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      <div className="product-name">{product.model}</div>
      <div className="product-brand">{product.brand_name}</div>
      <div className="product-specs">
        <div>Price: ₹{product.price}</div>
        <div>OS: {product.os}</div>
        <div>Screen Size: {product.screen_size} inches</div>
        <div>Processor: {product.processor_brand}</div>
        <div>RAM: {product.ram_capacity} GB</div>
        <div>Internal Memory: {product.internal_memory} GB</div>
        <div>Rear Camera: {product.primary_camera_rear} MP</div>
        <div>Front Camera: {product.primary_camera_front} MP</div>
        <div>Battery: {product.battery_capacity} mAh</div>
        <div>Fast Charging: {product.fast_charging || "N/A"}</div>
        <div>5G Support: {product.is_5g ? "Yes" : "No"}</div>
        <div>Rating: {product.avg_rating}</div>
      </div>
    </div>
  );
}


