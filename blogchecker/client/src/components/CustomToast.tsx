import { CheckCircle, XCircle, Loader2 } from "lucide-react";

export const SuccessToast = ({ message }: { message: string }) => (
  <div className="flex items-center">
    <CheckCircle className="text-green-500 mr-2" />
    <span>{message}</span>
  </div>
);

export const ErrorToast = ({ message }: { message: string }) => (
  <div className="flex items-center">
    <XCircle className="text-red-500 mr-2" />
    <span>{message}</span>
  </div>
);

export const LoadingToast = ({ message }: { message: string }) => (
  <div className="flex items-center">
    <Loader2 className="text-gray-500 mr-2 animate-spin" />
    <span>{message}</span>
  </div>
);
